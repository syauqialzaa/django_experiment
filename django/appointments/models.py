from django.db import models
from django.conf import settings
from services.models import Service

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_patient')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    class Meta:
        unique_together = ('doctor', 'appointment_time')

    def __str__(self):
        return f"Appointment for {self.patient.username} at {self.appointment_time}"