from django.db import models
import uuid

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    
    plan = models.ForeignKey('subscriptions.SubscriptionPlan', on_delete=models.SET_NULL, null=True)
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='ETB')
    
    # Chapa specific fields
    tx_ref = models.CharField(max_length=100, unique=True) # Our unique reference
    chapa_ref = models.CharField(max_length=100, blank=True, null=True) # Chapa's reference
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tx_ref} - {self.status}"