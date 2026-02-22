from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):

    ROLE_CHOICES = (
        ('organizer', 'Organizer'),
        ('volunteer', 'Volunteer'),
        ('participant', 'Participant'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    organization = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='participant'
    )

    is_email_verified = models.BooleanField(default=False)
    is_active_member = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
