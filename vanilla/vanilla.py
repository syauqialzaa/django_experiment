import http.server
import socketserver
import json
import psycopg2
from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Load environment variables from .env
load_dotenv()

url: str = os.environ.get("URL")
key: str = os.environ.get("KEY")
supabase: Client = create_client(url, key)
db = supabase.schema("public")

class MyHandler(http.server.SimpleHTTPRequestHandler):

    def _read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def _send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def _norm(self):
        # normalize path: strip query + trailing slash
        return self.path.split("?", 1)[0].rstrip("/") or "/"

    # ------------- routing -------------
    def do_POST(self):
        path = self._norm()
        if path == "/login":
            return self.login()
        elif path == "/signup":
            return self.signup()
        # services create
        elif path == "/api/services":
            return self.create_service()
        elif path == "/api/appointments/book":
            return self.book_appointment()
        elif path.startswith("/api/appointments/") and path.endswith("/cancel"):
            return self.cancel_appointment()
        else:
            return self._send_json(404, {"error": "Not found"})
        
    def do_GET(self):
        path = self._norm()
        # user detail (existing)
        if path.startswith("/users/"):
            return self.get_user()
        # services list
        if path == "/api/services":
            return self.list_services()
        # services detail
        if path.startswith("/api/services/"):
            return self.get_service()
        if path == "/api/appointments":
            return self.list_appointments()
        return self._send_json(404, {"error": "Not found"})

    def do_PUT(self):
        path = self._norm()
        # services PUT /api/services/{id}
        if path.startswith("/api/services/"):
            return self.update_service()
        # NEW: user PUT /api/user/{id}/update
        if path.startswith("/api/user/") and path.endswith("/update"):
            return self.update_user()
        return self._send_json(404, {"error": "Not found"})

    def do_DELETE(self):
        path = self._norm()
        # user delete (existing)
        if path.startswith("/user/") and path.endswith("/delete"):
            return self.delete_user()
        # services delete
        if path.startswith("/api/services/"):
            return self.delete_service()
        return self._send_json(404, {"error": "Not found"})

    # ------------- USERS (your existing endpoints) -------------
    def signup(self):
        data = self._read_json()
        required = ("username", "email", "password", "role")
        if not data or any(k not in data or not data[k] for k in required):
            return self._send_json(400, {"error": "Missing fields: username, email, password, role"})
        if data["role"] not in ("consumer", "doctor"):
            return self._send_json(400, {"error": "role must be 'consumer' or 'doctor'"})
        try:
            db.table("users").insert({
                "username": data["username"],
                "email": data["email"],
                "password": data["password"],  # hash in prod
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
                return self._send_json(500, {"error": "User created but not returned"})
            return self._send_json(201, {"user": rows[0]})
        except Exception as e:
            return self._send_json(400, {"error": f"Supabase error: {e}"})

    def update_user(self):
        path = self._norm()
        parts = path.split("/")
        if len(parts) != 4 or parts[1] != "user" or parts[3] != "update":
            return self._send_json(404, {"error": "Not found"})
        user_id = parts[2]
        if not user_id.isdigit():
            return self._send_json(400, {"error": "Invalid user id"})

        data = self._read_json() or {}
        patch = {k: v for k, v in data.items() if k in ("username", "email", "password", "role")}
        if "role" in patch and patch["role"] not in ("consumer", "doctor"):
            return self._send_json(400, {"error": "role must be 'consumer' or 'doctor'"})
        if not patch:
            return self._send_json(400, {"error": "No updatable fields provided"})

        try:
            db.table("users").update(patch).eq("id", int(user_id)).execute()
            res = (
                db.table("users")
                .select("id,username,email,role")
                .eq("id", int(user_id))
                .limit(1)
                .execute()
            )
            rows = res.data or []
            if not rows:
                return self._send_json(404, {"error": "User not found"})
            return self._send_json(200, {"user": rows[0]})
        except Exception as e:
            return self._send_json(400, {"error": f"Supabase error: {e}"})

    def delete_user(self):
        path = self._norm()
        parts = path.split("/")
        if len(parts) != 4 or parts[1] != "user" or parts[3] != "delete":
            return self._send_json(404, {"error": "Not found"})
        user_id = parts[2]
        if not user_id.isdigit():
            return self._send_json(400, {"error": "Invalid user id"})
        try:
            db.table("users").delete().eq("id", int(user_id)).execute()
            return self._send_json(200, {"status": "deleted", "id": int(user_id)})
        except Exception as e:
            return self._send_json(400, {"error": f"Supabase error: {e}"})

    def get_user(self):
        path = self._norm()
        parts = path.split("/")
        if len(parts) != 3 or parts[1] != "users":
            return self._send_json(404, {"error": "Not found"})
        user_id = parts[2]
        if not user_id.isdigit():
            return self._send_json(400, {"error": "Invalid user id"})
        try:
            response = (
                db.table("users")
                .select("id, username, role")  # do NOT return password
                .eq("id", int(user_id))
                .limit(1)
                .execute()
            )
            rows = response.data or []
            if not rows:
                return self._send_json(404, {"error": "User not found"})
            return self._send_json(200, {"user": rows[0]})
        except Exception as e:
            return self._send_json(500, {"error": f"Supabase error: {e}"})

    def login(self):
        data = self._read_json()
        if not data or "username" not in data or "password" not in data:
            return self._send_json(400, {"error": "Missing username or password"})
        username = data["username"]
        password = data["password"]
        try:
            response = (
                db.table("users")
                .select("id, username, role")
                .eq("username", username)
                .eq("password", password)
                .limit(1)
                .execute()
            )
            rows = response.data or []
            if rows:
                return self._send_json(200, {"status": "success", "user": rows[0]})
            else:
                return self._send_json(401, {"status": "fail", "error": "Invalid credentials"})
        except Exception as e:
            return self._send_json(500, {"error": f"Supabase error: {e}"})

    # ------------- SERVICES (new endpoints) -------------
    # GET /api/services/
    def list_services(self):
        try:
            res = db.table("services").select("id,name,hospital_id").execute()
            services = res.data or []
            out = [self._hydrate_service_row(s) for s in services]
            return self._send_json(200, {"services": out})
        except Exception as e:
            return self._send_json(500, {"error": f"Supabase error: {e}"})

    # POST /api/services/  {hospital_id, name}
    def create_service(self):
        data = self._read_json() or {}
        if "hospital_id" not in data or "name" not in data:
            return self._send_json(400, {"error": "Missing fields: hospital_id, name"})
        try:
            # validate hospital
            h = db.table("hospitals").select("id").eq("id", data["hospital_id"]).limit(1).execute()
            if not (h.data or []):
                return self._send_json(400, {"error": "hospital_id not found"})

            db.table("services").insert({
                "hospital_id": data["hospital_id"],
                "name": data["name"],
            }).execute()

            created = (
                db.table("services")
                .select("id,name,hospital_id")
                .eq("hospital_id", data["hospital_id"])
                .eq("name", data["name"])
                .limit(1)
                .execute()
            )
            rows = created.data or []
            if not rows:
                return self._send_json(201, {"message": "created"})
            return self._send_json(201, {"service": self._hydrate_service_row(rows[0])})
        except Exception as e:
            return self._send_json(400, {"error": f"Supabase error: {e}"})

    # GET /api/services/{id}/
    def get_service(self):
        path = self._norm()
        parts = path.split("/")
        # expected ["", "api", "services", "{id}"]
        if len(parts) != 4 or not parts[3].isdigit():
            return self._send_json(404, {"error": "Not found"})
        service_id = int(parts[3])
        try:
            res = (
                db.table("services")
                .select("id,name,hospital_id")
                .eq("id", service_id)
                .limit(1)
                .execute()
            )
            rows = res.data or []
            if not rows:
                return self._send_json(404, {"error": "Service not found"})
            return self._send_json(200, {"service": self._hydrate_service_row(rows[0])})
        except Exception as e:
            return self._send_json(500, {"error": f"Supabase error: {e}"})

    # PUT /api/services/{id}/  {hospital_id?, name?}
    def update_service(self):
        path = self._norm()
        parts = path.split("/")
        if len(parts) != 4 or not parts[3].isdigit():
            return self._send_json(404, {"error": "Not found"})
        service_id = int(parts[3])
        data = self._read_json() or {}
        patch = {k: v for k, v in data.items() if k in ("hospital_id", "name")}
        if not patch:
            return self._send_json(400, {"error": "No updatable fields provided (hospital_id, name)"})
        try:
            if "hospital_id" in patch:
                h = db.table("hospitals").select("id").eq("id", patch["hospital_id"]).limit(1).execute()
                if not (h.data or []):
                    return self._send_json(400, {"error": "hospital_id not found"})
            db.table("services").update(patch).eq("id", service_id).execute()

            res = (
                db.table("services")
                .select("id,name,hospital_id")
                .eq("id", service_id)
                .limit(1)
                .execute()
            )
            rows = res.data or []
            if not rows:
                return self._send_json(404, {"error": "Service not found"})
            return self._send_json(200, {"service": self._hydrate_service_row(rows[0])})
        except Exception as e:
            return self._send_json(400, {"error": f"Supabase error: {e}"})

    # DELETE /api/services/{id}/
    def delete_service(self):
        path = self._norm()
        parts = path.split("/")
        if len(parts) != 4 or not parts[3].isdigit():
            return self._send_json(404, {"error": "Not found"})
        service_id = int(parts[3])
        try:
            db.table("services").delete().eq("id", service_id).execute()
            return self._send_json(200, {"status": "deleted", "id": service_id})
        except Exception as e:
            return self._send_json(400, {"error": f"Supabase error: {e}"})

    # ----- helpers for services -----
    def _hydrate_service_row(self, svc_row: dict):
        # hospital name
        hospital_name = None
        if svc_row.get("hospital_id") is not None:
            hres = db.table("hospitals").select("id,name").eq("id", svc_row["hospital_id"]).limit(1).execute()
            if hres.data:
                hospital_name = hres.data[0]["name"]
        # doctors (from schedule rows for this service)
        doctors = self._get_doctors_for_service(svc_row.get("id"))
        return {
            "id": svc_row.get("id"),
            "name": svc_row.get("name"),
            "hospital": {"id": svc_row.get("hospital_id"), "name": hospital_name},
            "doctors": doctors,
        }

    def _get_doctors_for_service(self, service_id: int):
        if not service_id:
            return []
        try:
            sched = db.table("schedule").select("doctor_id").eq("service_id", service_id).execute()
            srows = sched.data or []
            if not srows:
                return []
            doctor_ids = sorted({r["doctor_id"] for r in srows if r.get("doctor_id") is not None})
            if not doctor_ids:
                return []
            users_res = (
                db.table("users")
                .select("id,username,role")
                .in_("id", doctor_ids)
                .eq("role", "doctor")
                .execute()
            )
            return [{"id": u["id"], "username": u["username"]} for u in (users_res.data or [])]
        except Exception:
            return []
        
         # ---------- APPOINTMENTS ----------
    # GET /api/appointments/
    def list_appointments(self):
        try:
            res = db.table("appointments").select("id,schedule_id,status,created_at").execute()
            return self._send_json(200, {"appointments": (res.data or [])})
        except Exception as e:
            return self._send_json(500, {"error": f"Supabase error: {e}"})

    # POST /api/appointments/book  { "schedule_id": <int> }
    def book_appointment(self):
        data = self._read_json() or {}
        if "schedule_id" not in data or not str(data["schedule_id"]).isdigit():
            return self._send_json(400, {"error": "Missing or invalid schedule_id"})
        schedule_id = int(data["schedule_id"])

        try:
            # Ensure schedule exists
            s = db.table("schedule").select("id").eq("id", schedule_id).limit(1).execute()
            if not (s.data or []):
                return self._send_json(400, {"error": "schedule_id not found"})

            # Find or create appointment row for this schedule
            ap = db.table("appointments").select("id,status,schedule_id").eq("schedule_id", schedule_id).limit(1).execute()
            if not (ap.data or []):
                # create as available
                db.table("appointments").insert({"schedule_id": schedule_id}).execute()
                ap = db.table("appointments").select("id,status,schedule_id").eq("schedule_id", schedule_id).limit(1).execute()

            appt = ap.data[0]
            if appt["status"] != "available":
                return self._send_json(409, {"error": "Slot already booked", "appointment": appt})

            # Book it
            db.table("appointments").update({"status": "booked"}).eq("id", appt["id"]).execute()
            fresh = db.table("appointments").select("id,schedule_id,status,created_at").eq("id", appt["id"]).limit(1).execute()
            return self._send_json(200, {"appointment": (fresh.data or [])[0]})
        except Exception as e:
            return self._send_json(400, {"error": f"Supabase error: {e}"})

    # POST /api/appointments/{appointment_id}/cancel
    def cancel_appointment(self):
        path = self._norm()
        parts = path.split("/")
        # ["", "api", "appointments", "{id}", "cancel"]
        if len(parts) != 5 or not parts[3].isdigit():
            return self._send_json(404, {"error": "Not found"})
        appt_id = int(parts[3])

        try:
            ap = db.table("appointments").select("id,status,schedule_id").eq("id", appt_id).limit(1).execute()
            rows = ap.data or []
            if not rows:
                return self._send_json(404, {"error": "Appointment not found"})
            appt = rows[0]

            # This implementation re-opens the slot by setting status back to 'available'.
            db.table("appointments").update({"status": "available"}).eq("id", appt_id).execute()
            fresh = db.table("appointments").select("id,schedule_id,status,created_at").eq("id", appt_id).limit(1).execute()
            return self._send_json(200, {"appointment": (fresh.data or [])[0]})
        except Exception as e:
            return self._send_json(400, {"error": f"Supabase error: {e}"})
        
Handler = MyHandler

try:
    with socketserver.TCPServer(("", 8000), Handler) as httpd:
        print(f"Starting http://0.0.0.0:{8000}")
        httpd.serve_forever()
except KeyboardInterrupt:   
    print("Stopping by Ctrl+C")
    httpd.server_close()