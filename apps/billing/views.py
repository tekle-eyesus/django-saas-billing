from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.subscriptions.models import SubscriptionPlan
from .services import ChapaService
import hmac
import hashlib
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.subscriptions.models import Subscription
from .models import Transaction


class InitializePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Get the plan they want to buy
        plan_slug = request.data.get('plan_slug')
        plan = get_object_or_404(SubscriptionPlan, slug=plan_slug)

        # 2. Get the user's organization
        user = request.user
        if not user.organization:
            return Response({"error": "User does not belong to an organization"}, status=400)

        # 3. Generate a unique Transaction Reference
        tx_ref = ChapaService.generate_tx_ref()

        # 4. Create a local Transaction record (Pending)
        Transaction.objects.create(
            organization=user.organization,
            user=user,
            plan=plan,
            amount=plan.price,
            currency='ETB',
            tx_ref=tx_ref,
            status='PENDING'
        )

        # 5. Call Chapa to get the Checkout URL
        chapa = ChapaService()
        checkout_url = chapa.initialize_payment(
            email=user.email,
            amount=plan.price,
            first_name=user.first_name,
            last_name=user.last_name,
            tx_ref=tx_ref,
            return_url="http://localhost:3000/payment-success" # Frontend URL
        )

        if checkout_url:
            return Response({
                "checkout_url": checkout_url,
                "tx_ref": tx_ref
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to initialize payment"}, status=500)
        

class ChapaWebhookView(APIView):
    """
    Receives payment confirmation from Chapa and updates subscription.
    """
    authentication_classes = [] # Webhooks are public endpoints
    permission_classes = []

    def post(self, request):
        signature = request.headers.get('x-chapa-signature')
        secret = settings.CHAPA_WEBHOOK_SECRET
        
        if secret and signature:
            # Hash the request body using your secret
            expected_signature = hmac.new(
                secret.encode('utf-8'), 
                request.body, 
                hashlib.sha256
            ).hexdigest()
            
            if expected_signature != signature:
                return Response({"error": "Invalid Signature"}, status=status.HTTP_403_FORBIDDEN)

     
        data = request.data
        tx_ref = data.get('tx_ref') or data.get('data', {}).get('tx_ref')
        
        if not tx_ref:
            return Response({"error": "tx_ref missing"}, status=400)

     
        try:
            transaction = Transaction.objects.get(tx_ref=tx_ref)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

       
        if transaction.status == 'SUCCESS':
            return Response({"message": "Already processed"}, status=200)

        # Mark Transaction as SUCCESS
        transaction.status = 'SUCCESS'
        transaction.chapa_ref = data.get('reference', '') 
        transaction.save()

        organization = transaction.organization
        plan = transaction.plan
        
        new_end_date = timezone.now() + timedelta(days=30)

        subscription, created = Subscription.objects.get_or_create(
            organization=organization,
            defaults={
                'plan': plan,
                'end_date': new_end_date,
                'status': 'ACTIVE'
            }
        )

        if not created:
            # If they already had a sub, upgrade/renew it
            subscription.plan = plan
            subscription.status = 'ACTIVE'
            subscription.end_date = new_end_date
            subscription.save()

        return Response({"status": "success"}, status=200)