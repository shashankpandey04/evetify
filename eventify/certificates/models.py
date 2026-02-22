from django.db import models
from accounts.models import User
from events.models import Event

class CertificatesModel(models.Model):
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    issuedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_certificates')
    issueDate = models.DateField()
    issuedTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_certificates', null=True, blank=True)