"""
URL configuration for hospital_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from api.views import user, service, appointment


urlpatterns = [
   # user
    path("signup", user.signup),                         # POST
    path("login", user.login),                           # POST
    path("users/<int:user_id>", user.get_user),          # GET
    path("users/<int:user_id>/delete", user.delete_user), # DELETE
    path("api/users/<int:user_id>/update", user.update_user_put),  # PUT

    # service
    path("api/services/", service.services_collection),          # GET (list) / POST (create)
    path("api/services/<int:service_id>", service.service_item), # GET / PUT / DELETE

    # appointment
    path("api/appointments/", appointment.list_appointments),              # GET
    path("api/appointments/book", appointment.book_appointment),           # POST
    path("api/appointments/<int:appointment_id>/cancel", appointment.cancel_appointment),  # POST
]
