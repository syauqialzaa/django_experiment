from django.urls import path
from . import views

urlpatterns = [
    # maps to /api/appointments/book/ (POST for book)
    path('appointments/book/', views.book_appointment, name='book-appointment'),
    
    # Maps to /api/appointments/{appointment_id}/ (POST for cancel)
    path('appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel-appointment'),
    
    # Maps to /api/appointments/ (GET for list)
    path('appointments/', views.list_appointments, name='list-appointments'),
]