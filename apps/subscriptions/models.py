from django.db import models
from django.utils import timezone
from datetime import timedelta

class SubscriptionPlan(models.Model):
    """
    Defines the tiers available in your SaaS.
    """
    name = models.CharField(max_length=50)  # e.g., "Basic", "Pro"
    slug = models.SlugField(unique=True)    # e.g., "basic", "pro"
    price = models.DecimalField(max_digits=10, decimal_places=2) # e.g., 500.00
    currency = models.CharField(max_length=3, default='ETB')
    
    # Limits & Quotas (Crucial for SaaS)
    max_members = models.PositiveIntegerField(default=1)
    max_api_calls_per_day = models.PositiveIntegerField(default=100)
    
    # Integration IDs (For Chapa/Stripe mapping later)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)
    chapa_plan_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.price} {self.currency})"


class Subscription(models.Model):
    """
    Tracks the active plan for an Organization.
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAST_DUE', 'Past Due'),
        ('CANCELED', 'Canceled'),
        ('INCOMPLETE', 'Incomplete'), # Waiting for payment
    ]

    # One Organization can only have ONE active subscription at a time
    organization = models.OneToOneField(
        'organizations.Organization', 
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INCOMPLETE')
    
    # Billing cycle tracking
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    
    # Payment Reference (Last successful transaction ID)
    reference = models.CharField(max_length=100, blank=True, null=True)

    def is_valid(self):
        """Helper to check if sub is valid right now"""
        return self.status == 'ACTIVE' and self.end_date > timezone.now()

    def __str__(self):
        return f"{self.organization.name} - {self.plan.name}"