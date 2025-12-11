from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.subscriptions.throttling import SubscriptionRateThrottle

class DashboardAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [SubscriptionRateThrottle]

    def get(self, request):
        # This simulates a heavy data request
        return Response({
            "message": "Here is your expensive analytics data.",
            "organization": request.user.organization.name,
            "plan_limit": f"Your plan allows {self.request.user.organization.subscription.plan.max_api_calls_per_day} calls/day"
        })