import json
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import User, ApiToken
from .decorators import token_required

@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'patient')

        if not all([username, password, email]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_http_methods(["GET"]) # WARNING: Insecure. Use POST in a real application.
def login_view(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, _ = ApiToken.objects.get_or_create(user=user)
        return JsonResponse({'token': str(token.key), 'user_id': user.id, 'role': user.role})
    
    return JsonResponse({'error': 'Invalid Credentials'}, status=401)

@csrf_exempt
@token_required
@require_http_methods(["GET", "PUT", "DELETE"])
def user_detail_view(request, user_id):
    # The @token_required decorator has already attached the authenticated user to request.user
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Check permissions
    if request.user.id != user.id and request.user.role != 'administrator':
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if request.method == 'GET':
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        })

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user.email = data.get('email', user.email)
            user.role = data.get('role', user.role) # Admins might change roles
            user.save()
            return JsonResponse({'message': 'User updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)
