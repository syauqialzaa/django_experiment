# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # For simplicity in this example
from .models import User, Service
from .serializers import user_to_dict, service_to_dict

def user_detail_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse(user_to_dict(user))
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt # In a real app, use proper CSRF handling
def service_list_create_view(request):
    if request.method == 'GET':
        services = Service.objects.select_related('doctor').all()
        data = [service_to_dict(s) for s in services]
        return JsonResponse(data, safe=False)
    
    # --- POST logic (DILENGKAPI) ---
    if request.method == 'POST':
        # Simple authorization check: assume user info is in headers or session
        # For this example, we'll just check the doctor_id from the payload
        try:
            data = json.loads(request.body)
            doctor_id = data.get('doctor_id')
            doctor = User.objects.get(pk=doctor_id, role='doctor')
            
            new_service = Service.objects.create(
                name=data['name'],
                clinic_name=data['clinic_name'],
                doctor=doctor
            )
            return JsonResponse(service_to_dict(new_service), status=201)
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'Doctor not found or user is not a doctor'}, status=403)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid or missing data'}, status=400)