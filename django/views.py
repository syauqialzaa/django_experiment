# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import User, Service, Appointment

# ADDED: View for user registration
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Use the custom manager's create_user method
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                role=data.get('role', 'patient') # Default to 'patient'
            )
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Could not create user: {e}'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

# ADDED: View for user login
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = authenticate(
                request, 
                username=data['username'], 
                password=data['password']
            )
            if user is not None:
                # In a real app, you would start a session or issue a token (e.g., JWT) here
                return JsonResponse({'message': 'Login successful', 'user_id': user.id})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def cancel_appointment_view(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            # Here you might add an authorization check (e.g., is request.user the patient?)
            if appointment.cancel():
                return JsonResponse({'message': 'Appointment cancelled successfully'})
            else:
                return JsonResponse({'error': 'Appointment could not be cancelled (it may already be completed or cancelled)'}, status=400)
        except Appointment.DoesNotExist:
            return JsonResponse({'error': 'Appointment not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def user_appointments_view(request, user_id):
    """Example of a more complex query using the ORM."""
    try:
        user = User.objects.get(pk=user_id)
        # Efficiently fetch related data in one query
        appointments = Appointment.objects.filter(patient=user).select_related('service', 'service__doctor')
        
        data = [{
            'id': app.id,
            'date': app.appointment_date,
            'status': app.status,
            'service_name': app.service.name,
            'doctor_name': app.service.doctor.get_full_name() or app.service.doctor.username
        } for app in appointments]
        
        return JsonResponse(data, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)