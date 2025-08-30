import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from users.decorators import token_required
from users.models import User
from .models import Service, Clinic

@csrf_exempt
@token_required
@require_http_methods(["GET", "POST"])
def service_list_create_view(request):
    """
    Handles listing all services (GET) and creating a new one (POST).
    """
    # GET: List all services
    if request.method == 'GET':
        services = Service.objects.all()
        data = []
        for service in services:
            data.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'clinic': {
                    'id': service.clinic.id,
                    'name': service.clinic.name,
                },
                'doctors': [{'id': doc.id, 'username': doc.username} for doc in service.doctors.all()]
            })
        return JsonResponse(data, safe=False, status=200)

    # POST: Create a new service
    elif request.method == 'POST':
        # Authorization: Only administrators or doctors can create services.
        if request.user.role not in ['administrator', 'doctor']:
            return JsonResponse({'error': 'Forbidden: You do not have permission to create a service.'}, status=403)

        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description')
            clinic_id = data.get('clinic_id')
            doctor_ids = data.get('doctor_ids') # Expects a list of doctor IDs

            if not all([name, description, clinic_id, doctor_ids]):
                return JsonResponse({'error': 'Missing required fields: name, description, clinic_id, doctor_ids'}, status=400)

            # Validate clinic and doctors
            clinic = Clinic.objects.get(pk=clinic_id)
            doctors = User.objects.filter(pk__in=doctor_ids, role='doctor')
            
            if len(doctor_ids) != doctors.count():
                 return JsonResponse({'error': 'One or more invalid doctor IDs provided.'}, status=400)

            service = Service.objects.create(name=name, description=description, clinic=clinic)
            service.doctors.set(doctors) # Set the many-to-many relationship

            return JsonResponse({
                'message': 'Service created successfully',
                'service_id': service.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Clinic.DoesNotExist:
            return JsonResponse({'error': f'Clinic with ID {clinic_id} not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)


@csrf_exempt
@token_required
@require_http_methods(["GET", "PUT", "DELETE"])
def service_detail_view(request, service_id):
    """
    Handles retrieving (GET), updating (PUT), and deleting (DELETE) a specific service.
    """
    try:
        service = Service.objects.get(pk=service_id)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)

    # GET: Retrieve a single service's details
    if request.method == 'GET':
        return JsonResponse({
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'clinic': {
                'id': service.clinic.id,
                'name': service.clinic.name
            },
            'doctors': [{'id': doc.id, 'username': doc.username} for doc in service.doctors.all()]
        }, status=200)

    # Authorization check for PUT and DELETE
    if request.user.role not in ['administrator', 'doctor']:
        return JsonResponse({'error': 'Forbidden: You do not have permission to modify this service.'}, status=403)

    # PUT: Update an existing service
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            # Update fields if they are provided in the request body
            service.name = data.get('name', service.name)
            service.description = data.get('description', service.description)

            if 'clinic_id' in data:
                clinic = Clinic.objects.get(pk=data['clinic_id'])
                service.clinic = clinic

            if 'doctor_ids' in data:
                doctors = User.objects.filter(pk__in=data['doctor_ids'], role='doctor')
                service.doctors.set(doctors)

            service.save()
            return JsonResponse({'message': 'Service updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Clinic.DoesNotExist:
            return JsonResponse({'error': 'Clinic not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    # DELETE: Remove a service
    elif request.method == 'DELETE':
        service.delete()
        # A 204 response should not have a body
        return JsonResponse({'message': 'Service deleted successfully'}, status=204)