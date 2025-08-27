from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .utils.db import db
from .utils.utils import read_json, bad_request

def list_appointments(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error":"Not found"}, status=404)
    try:
        res = db.table("appointments").select("id,schedule_id,status,created_at").execute()
        return JsonResponse({"appointments": (res.data or [])})
    except Exception as e:
        return JsonResponse({"error": f"Supabase error: {e}"}, status=500)

@csrf_exempt
def book_appointment(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error":"Not found"}, status=404)
    data = read_json(request) or {}
    if "schedule_id" not in data or not str(data["schedule_id"]).isdigit():
        return bad_request("Missing or invalid schedule_id")
    schedule_id = int(data["schedule_id"])
    try:
        s = db.table("schedule").select("id").eq("id", schedule_id).limit(1).execute()
        if not (s.data or []):
            return bad_request("schedule_id not found")

        ap = db.table("appointments").select("id,status,schedule_id").eq("schedule_id", schedule_id).limit(1).execute()
        if not (ap.data or []):
            db.table("appointments").insert({"schedule_id": schedule_id}).execute()
            ap = db.table("appointments").select("id,status,schedule_id").eq("schedule_id", schedule_id).limit(1).execute()

        appt = ap.data[0]
        if appt["status"] != "available":
            return JsonResponse({"error":"Slot already booked","appointment":appt}, status=409)

        db.table("appointments").update({"status":"booked"}).eq("id", appt["id"]).execute()
        fresh = db.table("appointments").select("id,schedule_id,status,created_at").eq("id", appt["id"]).limit(1).execute()
        return JsonResponse({"appointment": (fresh.data or [])[0]})
    except Exception as e:
        return JsonResponse({"error": f"Supabase error: {e}"}, status=400)

@csrf_exempt
def cancel_appointment(request: HttpRequest, appointment_id: int):
    if request.method != "POST":
        return JsonResponse({"error":"Not found"}, status=404)
    try:
        ap = db.table("appointments").select("id,status,schedule_id").eq("id", appointment_id).limit(1).execute()
        rows = ap.data or []
        if not rows:
            return JsonResponse({"error":"Appointment not found"}, status=404)

        # re-open slot
        db.table("appointments").update({"status":"available"}).eq("id", appointment_id).execute()
        fresh = db.table("appointments").select("id,schedule_id,status,created_at").eq("id", appointment_id).limit(1).execute()
        return JsonResponse({"appointment": (fresh.data or [])[0]})
    except Exception as e:
        return JsonResponse({"error": f"Supabase error: {e}"}, status=400)
