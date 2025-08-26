from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from .models import User, Service, Appointment
import json

# --- Brief 1: Authentication & Authorization ---
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
        return JsonResponse({'message': 'User created', 'user_id': user.id}, status=201)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'GET': # As per brief, though POST is standard
        data = request.GET
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            # auth_login(request, user) # Session login
            return JsonResponse({'message': 'Login successful', 'user_id': user.id})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Invalid method'}, status=405)
    
def user_detail_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'role': user.role
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

# --- Brief 2: Service Management ---
@csrf_exempt
def service_list_create_view(request):
    if request.method == 'GET':
        services = Service.objects.all().values('name', 'clinic_name', 'doctor__username')
        return JsonResponse(list(services), safe=False)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        doctor = User.objects.get(pk=data['doctor_id'])
        service = Service.objects.create(
            name=data['name'],
            clinic_name=data['clinic_name'],
            doctor=doctor
        )
        return JsonResponse({'id': service.id, 'name': service.name}, status=201)

# --- Brief 3: Appointment Booking ---
@csrf_exempt
def book_appointment_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient = User.objects.get(pk=data['patient_id'])
        service = Service.objects.get(pk=data['service_id'])
        appointment = Appointment.objects.create(
            patient=patient,
            service=service,
            appointment_date=data['appointment_date']
        )
        return JsonResponse({'id': appointment.id, 'status': appointment.status}, status=201)

def appointment_list_view(request):
    appointments = Appointment.objects.all().select_related('patient', 'service').values(
        'id', 'patient__username', 'service__name', 'appointment_date', 'status'
    )
    return JsonResponse(list(appointments), safe=False)