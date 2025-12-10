from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.subscriptions.models import SubscriptionPlan
from .models import Transaction
from .services import ChapaService

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