import json
from django.http import JsonResponse, HttpRequest

def read_json(request: HttpRequest):
    try:
        body = request.body.decode("utf-8").strip()
        if not body:
            return None
        # tolerate accidental trailing ';'
        if body.endswith(";"):
            body = body[:-1].rstrip()
        return json.loads(body)
    except Exception:
        return None

def bad_request(msg="Bad request"):
    return JsonResponse({"error": msg}, status=400)
