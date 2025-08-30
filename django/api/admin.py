from django.contrib import admin
from .models import CustomUser, HealthFacility, Service, Appointment

# Mendaftarkan setiap model agar muncul di halaman admin
admin.site.register(CustomUser)
admin.site.register(HealthFacility)
admin.site.register(Service)
admin.site.register(Appointment)