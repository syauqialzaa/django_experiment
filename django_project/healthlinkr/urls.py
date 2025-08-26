"""
URL configuration for healthlinkr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Brief 1
    path('api/login/', views.login_view, name='login'),
    path('api/signup/', views.signup_view, name='signup'),
    path('api/user/<int:user_id>/', views.user_detail_view, name='user_detail'),

    # Brief 2
    path('api/services/', views.service_list_create_view, name='service_list_create'),
    path('api/services/<int:service_id>/', views.service_detail_view, name='service_detail'),

    # Brief 3
    path('api/appointments/', views.appointment_list_view, name='appointment_list'),
    path('api/appointments/book/', views.appointment_book_view, name='appointment_book'),
    path('api/appointments/<int:appointment_id>/cancel/', views.appointment_cancel_view, name='appointment_cancel'),
]
