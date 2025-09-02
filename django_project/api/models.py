from django.db import models
from uuid import uuid4
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(models.Model):
  id = models.UUIDField(primary_key=True, null=False, unique=True, default=uuid4)
  username = models.CharField(null=False, unique=True, max_length=20)
  email = models.EmailField(null=False, unique=True)
  ROLE_CHOICES = (
        ("administrator", "Administrator"),
        ("patient", "Patient"),
        ("doctor", "Doctor")
  )
  password = models.CharField(null=False, default="jenglot12345")
  role = models.CharField(
      max_length=20,
      choices=ROLE_CHOICES,
      default="patient"
  )
  created_at = models.DateTimeField(
      auto_now_add=True
  )

  def __str__(self):
      return self.username
  
class Service(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True
    )
    service_name = models.CharField(max_length=255, null=False)
    facility_name = models.CharField(max_length=255, null=False)
    list_doctor = ArrayField(
        models.CharField(max_length=255),
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)