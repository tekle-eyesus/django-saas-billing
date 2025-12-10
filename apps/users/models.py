from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """
    Custom User model with RBAC and Organization linkage.
    """
    OWNER = 'OWNER'     # Can manage billing & team
    ADMIN = 'ADMIN'     # Can manage content but not billing
    MEMBER = 'MEMBER'   # Read/Write access only
    
    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='members'
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email