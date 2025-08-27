from django.urls import path
from . import views

urlpatterns = [
    # Maps to /api/services/ (GET for list, POST for create)
    path('services/', views.service_list_create_view, name='service-list-create'),
    
    # Maps to /api/services/{service_id}/ (GET, PUT, DELETE for specific service)
    path('services/<int:service_id>/', views.service_detail_view, name='service-detail'),
]