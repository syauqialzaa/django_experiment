from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('administrator', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)

class ApiToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"