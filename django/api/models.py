from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Doctor'
        ADMINISTRATOR = 'administrator', 'Administrator'

    # Kita tidak butuh first_name, last_name, email bisa jadi username
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PATIENT)

    # Gunakan email untuk login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class HealthFacility(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='services')
    available_doctors = models.ManyToManyField(CustomUser, limit_choices_to={'role': CustomUser.Role.DOCTOR})

    def __str__(self):
        return f"{self.name} at {self.facility.name}"

class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)