import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import User, Service, Appointment
from django.forms.models import model_to_dict

# ==============================================================================
# Brief 1: Authentication & Authorization API
# ==============================================================================

@csrf_exempt
def login_view(request):
    if request.method == 'GET': # Sesuai brief, meskipun POST lebih umum untuk login
        try:
            data = json.loads(request.body)
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                return JsonResponse({"message": "Login successful", "user_id": user.id})
            else:
                return JsonResponse({"message": "Invalid credentials"}, status=401)
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"message": "Invalid JSON or missing fields"}, status=400)
    return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'patient')
        )
        return JsonResponse({"message": "User registered", "user_id": user.id}, status=201)
    return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def user_detail_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)

    if request.method == 'GET':
        user_data = {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
        return JsonResponse(user_data)

    if request.method == 'PUT':
        data = json.loads(request.body)
        user.email = data.get('email', user.email)
        user.save()
        return JsonResponse({"message": "User updated"})

    if request.method == 'DELETE':
        user.delete()
        return JsonResponse({"message": "User deleted"})

    return JsonResponse({"message": "Method not allowed"}, status=405)

# ==============================================================================
# Brief 2: Service Management API
# ==============================================================================

@csrf_exempt
def service_list_create_view(request):
    if request.method == 'GET':
        services = Service.objects.all().values('id', 'name', 'clinic_name', 'doctor__username')
        return JsonResponse(list(services), safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        doctor = User.objects.get(pk=data['doctor_id'])
        service = Service.objects.create(
            name=data['name'],
            clinic_name=data['clinic_name'],
            doctor=doctor
        )
        return JsonResponse({"message": "Service created", "id": service.id}, status=201)

@csrf_exempt
def service_detail_view(request, service_id):
    # Implementasi GET, PUT, DELETE untuk detail service (mirip user_detail_view)
    return JsonResponse({"message": "Endpoint not fully implemented yet"})

# ==============================================================================
# Brief 3: Appointment Booking & Management API
# ==============================================================================

@csrf_exempt
def appointment_list_view(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all().values()
        return JsonResponse(list(appointments), safe=False)

@csrf_exempt
def appointment_book_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient = User.objects.get(pk=data['user_id'])
        service = Service.objects.get(pk=data['service_id'])
        appointment = Appointment.objects.create(
            patient=patient,
            service=service,
            schedule=data['schedule']
        )
        return JsonResponse({"message": "Appointment booked", "id": appointment.id}, status=201)

@csrf_exempt
def appointment_cancel_view(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.status = 'cancelled'
            appointment.save()
            return JsonResponse({"message": "Appointment cancelled", "appointment": model_to_dict(appointment)})
        except Appointment.DoesNotExist:
            return JsonResponse({"message": "Appointment not found"}, status=404)
