from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .utils.db import db
from .utils.utils import read_json, bad_request

def _get_doctors_for_service(service_id: int):
    try:
        sched = db.table("schedule").select("doctor_id").eq("service_id", service_id).execute()
        srows = sched.data or []
        if not srows:
            return []
        ids = sorted({r["doctor_id"] for r in srows if r.get("doctor_id") is not None})
        if not ids:
            return []
        users_res = (
            db.table("users")
            .select("id,username,role")
            .in_("id", ids)
            .eq("role", "doctor")
            .execute()
        )
        return [{"id": u["id"], "username": u["username"]} for u in (users_res.data or [])]
    except Exception:
        return []

def _hydrate_service_row(svc_row: dict):
    hospital_name = None
    if svc_row.get("hospital_id") is not None:
        h = db.table("hospitals").select("id,name").eq("id", svc_row["hospital_id"]).limit(1).execute()
        if h.data:
            hospital_name = h.data[0]["name"]
    return {
        "id": svc_row.get("id"),
        "name": svc_row.get("name"),
        "hospital": {"id": svc_row.get("hospital_id"), "name": hospital_name},
        "doctors": _get_doctors_for_service(svc_row.get("id")),
    }

def services_collection(request: HttpRequest):
    if request.method == "GET":
        try:
            res = db.table("services").select("id,name,hospital_id").execute()
            out = [_hydrate_service_row(s) for s in (res.data or [])]
            return JsonResponse({"services": out})
        except Exception as e:
            return JsonResponse({"error": f"Supabase error: {e}"}, status=500)

    if request.method == "POST":
        data = read_json(request) or {}
        if "hospital_id" not in data or "name" not in data:
            return bad_request("Missing fields: hospital_id, name")
        try:
            h = db.table("hospitals").select("id").eq("id", data["hospital_id"]).limit(1).execute()
            if not (h.data or []):
                return bad_request("hospital_id not found")

            db.table("services").insert({"hospital_id": data["hospital_id"], "name": data["name"]}).execute()
            created = (
                db.table("services").select("id,name,hospital_id")
                .eq("hospital_id", data["hospital_id"]).eq("name", data["name"])
                .limit(1).execute()
            )
            rows = created.data or []
            if not rows:
                return JsonResponse({"message":"created"}, status=201)
            return JsonResponse({"service": _hydrate_service_row(rows[0])}, status=201)
        except Exception as e:
            return JsonResponse({"error": f"Supabase error: {e}"}, status=400)

    return JsonResponse({"error":"Not found"}, status=404)

def service_item(request: HttpRequest, service_id: int):
    if request.method == "GET":
        try:
            res = db.table("services").select("id,name,hospital_id").eq("id", service_id).limit(1).execute()
            rows = res.data or []
            if not rows:
                return JsonResponse({"error":"Service not found"}, status=404)
            return JsonResponse({"service": _hydrate_service_row(rows[0])})
        except Exception as e:
            return JsonResponse({"error": f"Supabase error: {e}"}, status=500)

    if request.method == "PUT":
        data = read_json(request) or {}
        patch = {k:v for k,v in data.items() if k in ("hospital_id","name")}
        if not patch:
            return bad_request("No updatable fields provided (hospital_id, name)")
        try:
            if "hospital_id" in patch:
                h = db.table("hospitals").select("id").eq("id", patch["hospital_id"]).limit(1).execute()
                if not (h.data or []):
                    return bad_request("hospital_id not found")
            db.table("services").update(patch).eq("id", service_id).execute()
            res = db.table("services").select("id,name,hospital_id").eq("id", service_id).limit(1).execute()
            rows = res.data or []
            if not rows:
                return JsonResponse({"error":"Service not found"}, status=404)
            return JsonResponse({"service": _hydrate_service_row(rows[0])})
        except Exception as e:
            return JsonResponse({"error": f"Supabase error: {e}"}, status=400)

    if request.method == "DELETE":
        try:
            db.table("services").delete().eq("id", service_id).execute()
            return JsonResponse({"status":"deleted","id":service_id})
        except Exception as e:
            return JsonResponse({"error": f"Supabase error: {e}"}, status=400)

    return JsonResponse({"error":"Not found"}, status=404)
