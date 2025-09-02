from rest_framework import serializers
from .models import User, Service

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "username", "email", "password", "role", "created_at"]
    extra_kwargs = {
      "password": {"write_only": True}
    }

class ServiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    fields = ["id", "service_name", "facility_name", "list_doctor", "created_at"]