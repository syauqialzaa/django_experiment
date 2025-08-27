# users/decorators.py
from functools import wraps
from django.http import JsonResponse
from .models import ApiToken

def token_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)

        token_key = auth_header.split(' ')[1]
        try:
            token = ApiToken.objects.get(key=token_key)
            request.user = token.user
        except ApiToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        return f(request, *args, **kwargs)
    return decorated_function