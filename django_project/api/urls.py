from django.urls import path
from .views import UserCreateView, UserLoginView, UserView, ServiceView, ServiceDetailView, AppointmentBook, AppointmentCancel


urlpatterns = [
    path('signup', UserCreateView.as_view(), name='auth'),
    path('login', UserLoginView.as_view(), name="auth"),
    path('users/<uuid:user_id>', UserView.as_view(), name="user_detail"),
    path('services', ServiceView.as_view(), name="services"),
    path('services/<uuid:service_id>', ServiceDetailView.as_view(), name="service_detail"),
    path('appointments', AppointmentBook.as_view(), name="appointments"),
    path('appointments/book', AppointmentBook.as_view(), name="appointments"),
    path('appointments/<uuid:appointment_id>/cancel', AppointmentCancel.as_view(), name="appointments")
]