import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# ==============================================================================
# In-Memory Database (sebagai pengganti database sungguhan)
# ==============================================================================
db = {
    "users": [
        {"id": 1, "username": "admin", "email": "admin@health.com", "password": "adminpassword", "role": "administrator"},
        {"id": 2, "username": "dr_strange", "email": "strange@health.com", "password": "doctorpassword", "role": "doctor"},
        {"id": 3, "username": "john_doe", "email": "john@patient.com", "password": "patientpassword", "role": "patient"},
    ],
    "services": [
        {"id": 1, "name": "Konsultasi Umum", "clinic_name": "Klinik Sehat Sentosa", "doctor_id": 2},
        {"id": 2, "name": "Pemeriksaan Gigi", "clinic_name": "Klinik Gigi Ceria", "doctor_id": 2},
    ],
    "appointments": [
        {"id": 1, "user_id": 3, "service_id": 1, "schedule": "2025-09-10T10:00:00Z", "status": "booked"},
    ]
}
# Helper untuk auto-increment ID
next_user_id = 4
next_service_id = 3
next_appointment_id = 2

# ==============================================================================
# Brief 1: Authentication & Authorization API
# ==============================================================================

@app.route('/api/login', methods=['GET'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    for user in db['users']:
        if user['username'] == username and user['password'] == password:
            return jsonify({"message": "Login successful", "user_id": user['id']}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    global next_user_id
    data = request.get_json()

    new_user = {
        "id": next_user_id,
        "username": data.get('username'),
        "email": data.get('email'),
        "password": data.get('password'),
        "role": data.get('role', 'patient') # Default role
    }
    db['users'].append(new_user)
    next_user_id += 1
    return jsonify({"message": "User registered successfully", "user": new_user}), 201

@app.route('/api/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(user_id):
    user = next((u for u in db['users'] if u['id'] == user_id), None)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if request.method == 'GET':
        return jsonify(user), 200

    if request.method == 'PUT':
        data = request.get_json()
        user['username'] = data.get('username', user['username'])
        user['email'] = data.get('email', user['email'])
        return jsonify({"message": "User updated", "user": user}), 200

    if request.method == 'DELETE':
        db['users'] = [u for u in db['users'] if u['id'] != user_id]
        return jsonify({"message": "User deleted"}), 200

# ==============================================================================
# Brief 2: Service Management API
# ==============================================================================

@app.route('/api/services', methods=['GET', 'POST'])
def handle_services():
    if request.method == 'GET':
        # Menambahkan detail dokter ke setiap service
        services_with_doctor = []
        for service in db['services']:
            doctor = next((u for u in db['users'] if u['id'] == service['doctor_id']), None)
            service_info = service.copy()
            service_info['doctor_name'] = doctor['username'] if doctor else "N/A"
            services_with_doctor.append(service_info)
        return jsonify(services_with_doctor), 200

    if request.method == 'POST':
        global next_service_id
        data = request.get_json()
        new_service = {
            "id": next_service_id,
            "name": data.get('name'),
            "clinic_name": data.get('clinic_name'),
            "doctor_id": data.get('doctor_id')
        }
        db['services'].append(new_service)
        next_service_id += 1
        return jsonify({"message": "Service created", "service": new_service}), 201

@app.route('/api/services/<int:service_id>', methods=['GET', 'PUT', 'DELETE'])
def service_detail(service_id):
    service = next((s for s in db['services'] if s['id'] == service_id), None)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    if request.method == 'GET':
        return jsonify(service), 200

    if request.method == 'PUT':
        data = request.get_json()
        service.update(data)
        return jsonify({"message": "Service updated", "service": service}), 200

    if request.method == 'DELETE':
        db['services'] = [s for s in db['services'] if s['id'] != service_id]
        return jsonify({"message": "Service deleted"}), 200

# ==============================================================================
# Brief 3: Appointment Booking & Management API
# ==============================================================================

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    return jsonify(db['appointments']), 200

@app.route('/api/appointments/book', methods=['POST'])
def book_appointment():
    global next_appointment_id
    data = request.get_json()
    new_appointment = {
        "id": next_appointment_id,
        "user_id": data.get('user_id'),
        "service_id": data.get('service_id'),
        "schedule": data.get('schedule'),
        "status": "booked"
    }
    db['appointments'].append(new_appointment)
    next_appointment_id += 1
    return jsonify({"message": "Appointment booked", "appointment": new_appointment}), 201

@app.route('/api/appointments/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    appointment = next((a for a in db['appointments'] if a['id'] == appointment_id), None)
    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404

    appointment['status'] = 'cancelled'
    # Logika untuk membuat slot tersedia kembali bisa ditambahkan di sini
    return jsonify({"message": "Appointment cancelled", "appointment": appointment}), 200

if __name__ == '__main__':
    app.run(debug=True)
