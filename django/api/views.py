from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import CustomUser, Service, Appointment

@csrf_exempt # Hanya untuk development, jangan di produksi!
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = CustomUser.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                role=data.get('role', 'patient')
            )
            return JsonResponse({'message': 'User created', 'user_id': user.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

def login(request):
    # Mengikuti brief menggunakan GET, meskipun POST lebih aman
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        # Django auth butuh request object, jadi kita tidak bisa pakai authenticate langsung
        # Ini cara manualnya, HINDARI DI PRODUKSI
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                 # Di aplikasi nyata, Anda akan membuat token di sini
                return JsonResponse({'message': 'Login successful', 'user_id': user.id})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

@csrf_exempt
def user_detail_update(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        data = {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.save()
        return JsonResponse({'message': 'User updated'})

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204) # No Content
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def services_list(request):
    if request.method == 'GET':
        services = Service.objects.all()
        data = []
        for service in services:
            doctors = [doc.username for doc in service.available_doctors.all()]
            data.append({
                'id': service.id,
                'name': service.name,
                'facility': service.facility.name,
                'doctors': doctors
            })
        return JsonResponse(data, safe=False)
    # Anda bisa tambahkan logika POST di sini
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def appointments_list(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        data = [
            {
                'id': app.id,
                'patient': app.patient.username,
                'doctor': app.doctor.username,
                'service': app.service.name,
                'time': app.appointment_time,
                'status': app.status
            } for app in appointments
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
