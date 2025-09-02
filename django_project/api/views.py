from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Service, Appointment
from .serializers import UserSerializer, ServiceSerializer, AppointmentSerializer
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
class UserCreateView(APIView):
  def post(self, request):
    data = request.data.copy()

    if "password" in data:
      data["password"] = make_password(data["password"])

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response({
        "status": "success",
        "message": "User created successfully",
        "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
      "status": "failed",
      "message": "Failed to create user",
      "errors": serializer.errors 
      }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
  def post(self, request):
    username = request.data.get("username")
    password = request.data.get("password")

    try:
      user = User.objects.filter(username=username).first()
      if not user:
        return Response({
          "status": "error",
          "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)
      
      # cek password
      if not check_password(password, user.password):
        return Response({
          "status": "error",
          "message": "Wrong password"
        }, status=status.HTTP_400_BAD_REQUEST)
      
      serializer = UserSerializer(user)

      return Response({
        "status": "success",
        "message": "User logged in successfully",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      return Response({
        "status": "error",
        "message": f"Failed to login: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UserView(APIView):
  def put(self, request, user_id):
    user = get_object_or_404(User, id=user_id)

    data = request.data.copy()

    if "password" in data:
      data["password"] = make_password(data["password"])

    serializer = UserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response({
        "status": "success",
        "message": "User updated successfully",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
    
    return Response({
      "status": "failed",
      "message": "Failed to update users",
      "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
  
  def get(self, request, user_id):
    try:
      user = get_object_or_404(User, id=user_id)
      serializer = UserSerializer(user)

      return Response({
        "status": "success",
        "message": "User fetched successfully",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to fetch users: {str(e)}",
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  def delete(self, request, user_id):
    try:
      user = get_object_or_404(User, id=user_id)
      user.delete()

      return Response({
        "status": "success",
        "message": "User deleted successfully"
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to delete user: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ServiceView(APIView):
  def post(self, request):
    try:
      serializer = ServiceSerializer(data=request.data)

      if serializer.is_valid():
        serializer.save()

        return Response({
          "status": "success",
          "message": "Service created successfully",
          "data": serializer.data
        }, status=status.HTTP_201_CREATED)
      
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to create service: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  def get(self, request):
    try:
      services = Service.objects.all()
      serializer = ServiceSerializer(services, many=True)

      return Response({
        "status": "success",
        "message": "Service fetch successfully",
        "data": serializer.data
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to fetch service: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class ServiceDetailView(APIView):
  def get(self, request, service_id):
    try:
      service = get_object_or_404(Service, id=service_id)
      serializer = ServiceSerializer(service)

      return Response({
        "status": "success",
        "message": "Service fetched successfully",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to fetch service: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  def delete(self, request, service_id):
    try:
      service = get_object_or_404(Service, id=service_id)
      service.delete()

      return Response({
        "status": "success",
        "message": "Service deleted successfully"
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to delete service: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  def put(self, request, service_id):
    try:
      service = get_object_or_404(Service, id=service_id)

      serializer = ServiceSerializer(service, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response({
          "status": "success",
          "message": "Service updated successfully",
          "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to update service: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class AppointmentBook(APIView):
  def post(self, request):
    try:
      serializer = AppointmentSerializer(data=request.data)

      if serializer.is_valid():
        serializer.save()
        return Response({
          "status": "success",
          "message": "Appointment created successfully",
          "data": serializer.data
        }, status=status.HTTP_201_CREATED)
      
      return Response({
        "status": "failed",
        "message": "Invalid appointment data",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to create appointment: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  def get(self, request):
    try:
      appointments = Appointment.objects.all()
      serializer = AppointmentSerializer(appointments, many=True)

      return Response({
        "status": "success",
        "message": "Appointments fetched successfully",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to fetch appointments: {str(e)}"
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AppointmentCancel(APIView):
  def post(self, request, appointment_id):
    try:
      appointment = get_object_or_404(Appointment, id=appointment_id)

      serializer = AppointmentSerializer(
        appointment, 
        data={"status":"cancelled"}, 
        partial=True
      )

      if serializer.is_valid():
        serializer.save()

        return Response({
          "status": "success",
          "message": "Appointment cancel successfully",
          "data": serializer.data
        }, status=status.HTTP_200_OK)
      
      return Response({
        "status": "failed",
        "message": "Failed to cancel appointment",
        "data": serializer.errors
      }, status=status.HTTP_200_OK)
    
    except Exception as e:
      return Response({
        "status": "failed",
        "message": f"Failed to cancel appointment: {str(e)}",
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)