from django.db import models
from events.models import Event
from accounts.models import User

class RegisterEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registeredAt = models.DateTimeField(auto_now_add=True)