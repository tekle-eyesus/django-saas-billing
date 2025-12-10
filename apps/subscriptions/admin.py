from django.contrib import admin
from .models import SubscriptionPlan, Subscription

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'max_api_calls_per_day')
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'plan', 'status', 'end_date', 'is_valid')
    list_filter = ('status', 'plan')