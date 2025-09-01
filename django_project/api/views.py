from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

# Create your views here.
class UsersView(APIView):
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({
        "status": "success",
        "message": "User created successfully",
        "data": serializer.data
        }, status=201)
    return Response({
      "status": "failed",
      "message": "Failed to create user",
      "errors": serializer.errors 
      }, status=400)