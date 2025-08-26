# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    
    # Appointment management endpoints
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment_view, name='cancel_appointment'),
    
    # User-specific data endpoints
    path('users/<int:user_id>/appointments/', views.user_appointments_view, name='user_appointments'),
]