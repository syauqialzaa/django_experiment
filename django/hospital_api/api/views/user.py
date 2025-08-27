from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .utils.db import db
from .utils.utils import read_json, bad_request

@csrf_exempt
def signup(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Not found"}, status=404)
    data = read_json(request)
    required = ("username","email","password","role")
    if not data or any(k not in data or not data[k] for k in required):
        return bad_request("Missing fields: username, email, password, role")
    if data["role"] not in ("consumer","doctor"):
        return bad_request("role must be 'consumer' or 'doctor'")
    try:
        db.table("users").insert({
            "username": data["username"],
            "email": data["email"],
            "password": data["password"],  # demo only; hash in prod
            "role": data["role"],
        }).execute()
        res = (
            db.table("users")
            .select("id,username,email,role")
            .eq("username", data["username"])
            .limit(1)
            .execute()
        )
        rows = res.data or []
        if not rows:
            return JsonResponse({"error":"User created but not returned"}, status=500)
        return JsonResponse({"user": rows[0]}, status=201)
    except Exception as e:
        return JsonResponse({"error": f"Supabase error: {e}"}, status=400)

@csrf_exempt
def login(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Not found"}, status=404)
    data = read_json(request)
    if not data or "username" not in data or "password" not in data:
        return bad_request("Missing username or password")
    try:
        res = (
            db.table("users")
            .select("id,username,role")
            .eq("username", data["username"])
            .eq("password", data["password"])
            .limit(1)
            .execute()
        )
        rows = res.data or []
        if rows:
            return JsonResponse({"status":"success","user":rows[0]})
        return JsonResponse({"status":"fail","error":"Invalid credentials"}, status=401)
    except Exception as e:
        return JsonResponse({"error": f"Supabase error: {e}"}, status=500)

def get_user(request: HttpRequest, user_id: int):
    if request.method != "GET":
        return JsonResponse({"error": "Not found"}, status=404)
    try:
        res = (
            db.table("users")
            .select("id,username,role")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )
        rows = res.data or []
        if not rows:
            return JsonResponse({"error":"User not found"}, status=404)
        return JsonResponse({"user": rows[0]})
    except Exception as e:
        return JsonResponse({"error": f"Supabase error: {e}"}, status=500)

@csrf_exempt
def delete_user(request: HttpRequest, user_id: int):
    if request.method != "DELETE":
        return JsonResponse({"error": "Not found"}, status=404)
    try:
        db.table("users").delete().eq("id", user_id).execute()
        return JsonResponse({"status":"deleted","id":user_id})
    except Exception as e:
        return JsonResponse({"error": f"Supabase error: {e}"}, status=400)

@csrf_exempt
def update_user_put(request: HttpRequest, user_id: int):
    if request.method != "PUT":
        return JsonResponse({"error": "Not found"}, status=404)
    data = read_json(request) or {}
    patch = {k:v for k,v in data.items() if k in ("username","email","password","role")}
    if "role" in patch and patch["role"] not in ("consumer","doctor"):
        return bad_request("role must be 'consumer' or 'doctor'")
    if not patch:
        return bad_request("No updatable fields provided")
    try:
        db.table("users").update(patch).eq("id", user_id).execute()
        res = (
            db.table("users")
            .select("id,username,email,role")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )
        rows = res.data or []
        if not rows:
            return JsonResponse({"error":"User not found"}, status=404)
        return JsonResponse({"user": rows[0]})
    except Exception as e:
        return JsonResponse({"error": f"Supabase error: {e}"}, status=400)
