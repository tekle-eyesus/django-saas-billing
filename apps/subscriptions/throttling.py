from rest_framework.throttling import UserRateThrottle

class SubscriptionRateThrottle(UserRateThrottle):
    scope = 'subscription'

    def get_rate(self):
        """
        FIX: We override this to return None.
        This prevents DRF from crashing because it can't find 'subscription' 
        in settings.py. We don't need a static setting because we set 
        self.rate dynamically in allow_request.
        """
        return None

    def allow_request(self, request, view):
        """
        We override allow_request because this is the moment we have access 
        to the 'request' object to check the user's plan.
        """
        if not request.user.is_authenticated:
            return True  # Let standard permission classes handle unauth users

        # 1. Calculate the limit dynamically from the DB
        daily_limit = self.get_plan_limit(request)

        # 2. Set the rate string manually (e.g., '100/day')
        self.rate = f'{daily_limit}/day'

        # 3. Tell DRF to parse this string into numbers (num_requests, duration)
        self.num_requests, self.duration = self.parse_rate(self.rate)

        # 4. Proceed with the standard throttling logic
        return super().allow_request(request, view)

    def get_plan_limit(self, request):
        """
        Helper to extract the integer limit from the DB.
        """
        default_limit = 10  # Fallback for users with no org/plan

        if not request.user.organization:
            return default_limit

        # Check for active subscription
        if hasattr(request.user.organization, 'subscription'):
            sub = request.user.organization.subscription
            # Ensure sub is valid (Active and not expired)
            if sub.is_valid():
                return sub.plan.max_api_calls_per_day
        
        return default_limit

    def get_cache_key(self, request, view):
        """
        Throttle based on Organization ID, not User ID.
        """
        if not request.user.is_authenticated or not request.user.organization:
            return None

        # The key tracks usage for the whole company
        return f'throttle_{self.scope}_{request.user.organization.id}'