from django.urls import path
from . import views

urlpatterns = [
    # Brief 1
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('user/<int:user_id>/', views.user_detail_view, name='user_detail'),
    
    # Brief 2
    path('services/', views.service_list_create_view, name='service_list_create'),
    
    # Brief 3
    path('appointments/book/', views.book_appointment_view, name='book_appointment'),
    path('appointments/', views.appointment_list_view, name='appointment_list'),
]