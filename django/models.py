# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone # ADDED for default date

# COMPLETED: Added create_superuser to make the manager fully functional
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # Handles hashing automatically
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Creates and saves a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'administrator') # Default role for superuser

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (('patient', 'Patient'), ('doctor', 'Doctor'), ('administrator', 'Administrator'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    
    # Use the custom manager
    objects = UserManager()

# ADDED: A complete Service model
class Service(models.Model):
    name = models.CharField(max_length=200)
    clinic_name = models.CharField(max_length=200)
    # The doctor for the service, limited to users with the 'doctor' role
    doctor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='services',
        limit_choices_to={'role': 'doctor'}
    )

    def __str__(self):
        return f"{self.name} by {self.doctor.username}"

# COMPLETED: A full Appointment model with fields and relationships
class Appointment(models.Model):
    STATUS_CHOICES = (('booked', 'Booked'), ('cancelled', 'Cancelled'), ('completed', 'Completed'))
    
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='appointments',
        limit_choices_to={'role': 'patient'}
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def cancel(self):
        """Business logic for cancelling an appointment."""
        # For example, an appointment cannot be cancelled if it's already completed
        if self.status == 'booked':
            self.status = 'cancelled'
            self.save()
            return True
        return False

    def __str__(self):
        return f"Appointment for {self.patient.username} on {self.appointment_date.strftime('%Y-%m-%d')}"