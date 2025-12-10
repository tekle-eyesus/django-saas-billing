from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_api_calls_per_day = models.IntegerField()
    stripe_price_id = models.CharField(max_length=100, blank=True)
    chapa_plan_id = models.CharField(max_length=100, blank=True)

class Subscription(models.Model):
    organization = models.OneToOneField('organizations.Organization', on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()