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

class Appointment(models.Model):
    class AppointmentStatus(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    patient = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="patient_appointments"
    )
    doctor = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE, related_name="appointments"
    )

    appointment_time = models.DateTimeField(null=False)
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.SCHEDULED,
    )
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    
