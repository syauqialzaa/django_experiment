from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('administrator', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

class Service(models.Model):
    name = models.CharField(max_length=200)
    clinic_name = models.CharField(max_length=200)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f"{self.name} at {self.clinic_name}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')

    def __str__(self):
        return f"Appointment for {self.patient.username} on {self.appointment_date}"