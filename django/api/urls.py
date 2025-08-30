from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('user/<int:user_id>/', views.user_detail_update), # Untuk GET
    path('user/<int:user_id>/update', views.user_detail_update), # Untuk PUT/DELETE
    path('services/', views.services_list),
    path('appointments/', views.appointments_list),
]