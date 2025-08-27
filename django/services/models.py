from django.db import models
from django.conf import settings

class Clinic(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    def __str__(self): return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='services')
    doctors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='services_offered', limit_choices_to={'role': 'doctor'}
    )
    def __str__(self): return f"{self.name} at {self.clinic.name}"