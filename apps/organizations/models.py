from django.db import models
import uuid

class Organization(models.Model):
    """
    Represents the Team/Company entity that holds the subscription.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    api_key = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name