from django.db import models
from django.conf import settings
import uuid
from accounts.models import User

class Event(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired")
    )

    eventID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    title = models.CharField(max_length=200)
    description = models.TextField()

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organized_events"
    )

    volunteers = models.ManyToManyField(
        User,
        blank=True,
        related_name="volunteered_events"
    )

    location = models.CharField(max_length=255)

    cityName = models.CharField(max_length=100)
    countryName = models.CharField(max_length=100)

    date = models.DateField()

    bannerUrl = models.URLField(max_length=500, blank=True, null=True)

    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    registrationDeadline = models.DateTimeField(null=True, blank=True)

    capacity = models.PositiveIntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    attendanceEnabled = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
