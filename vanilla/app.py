import hashlib
import database as db

app = Flask(__name__)

# ==============================
# --- Brief 1: Authentication & Authorization ---
# ==============================

@app.route('/api/signup/', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    
    if username in [u['username'] for u in db.users.values()]:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    
    new_user = {
        "id": db.user_id_counter,
        "username": username,
        "email": data.get('email'),
        "password_hash": hashed_password,
        "role": data.get('role', 'patient')
    }
    db.users[db.user_id_counter] = new_user
    db.user_id_counter += 1
    
    return jsonify({"message": "User created", "user_id": new_user['id']}), 201


@app.route('/api/login/', methods=['GET'])
def login():
    # Simplistic login for demonstration
    username = request.args.get('username')
    password = request.args.get('password')
    
    for user in db.users.values():
        if user['username'] == username:
            if user['password_hash'] == hashlib.sha256(password.encode()).hexdigest():
                return jsonify({"message": "Login successful", "user_id": user['id']}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/api/user/<int:user_id>/', methods=['GET'])
def get_user(user_id):
    user = db.users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user['id'],
        "username": user['username'],
        "email": user['email'],
        "role": user['role']
    })


@app.route('/api/user/<int:user_id>/', methods=['PUT'])
def update_user(user_id):
    user = db.users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    user['username'] = data.get('username', user['username'])
    user['email'] = data.get('email', user['email'])
    if data.get('password'):
        user['password_hash'] = hashlib.sha256(data['password'].encode()).hexdigest()
    user['role'] = data.get('role', user['role'])

    return jsonify({"message": "User updated", "user": user})


@app.route('/api/user/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in db.users:
        return jsonify({"error": "User not found"}), 404
    
    del db.users[user_id]
    return jsonify({"message": "User deleted"})


# ==============================
# --- Brief 2: Service Management ---
# ==============================

@app.route('/api/services/', methods=['POST'])
def create_service():
    data = request.json
    new_service = {
        "id": db.service_id_counter,
        "name": data['name'],
        "clinic_name": data['clinic_name'],
        "doctor_name": data['doctor_name']
    }
    db.services[db.service_id_counter] = new_service
    db.service_id_counter += 1
    return jsonify(new_service), 201


@app.route('/api/services/', methods=['GET'])
def get_services():
    return jsonify(list(db.services.values()))


@app.route('/api/services/<int:service_id>/', methods=['GET'])
def get_service(service_id):
    service = db.services.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    return jsonify(service)


@app.route('/api/services/<int:service_id>/', methods=['PUT'])
def update_service(service_id):
    service = db.services.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    data = request.json
    service['name'] = data.get('name', service['name'])
    service['clinic_name'] = data.get('clinic_name', service['clinic_name'])
    service['doctor_name'] = data.get('doctor_name', service['doctor_name'])

    return jsonify({"message": "Service updated", "service": service})


@app.route('/api/services/<int:service_id>/', methods=['DELETE'])
def delete_service(service_id):
    if service_id not in db.services:
        return jsonify({"error": "Service not found"}), 404
    
    del db.services[service_id]
    return jsonify({"message": "Service deleted"})


# ==============================
# --- Brief 3: Appointment Booking ---
# ==============================

@app.route('/api/appointments/book/', methods=['POST'])
def book_appointment():
    data = request.json
    
    # Basic validation
    if not db.users.get(data['patient_id']) or not db.services.get(data['service_id']):
        return jsonify({"error": "Invalid patient or service ID"}), 400

    new_appointment = {
        "id": db.appointment_id_counter,
        "patient_id": data['patient_id'],
        "service_id": data['service_id'],
        "date": data['date'],
        "status": "booked"
    }
    db.appointments[db.appointment_id_counter] = new_appointment
    db.appointment_id_counter += 1
    return jsonify(new_appointment), 201


@app.route('/api/appointments/', methods=['GET'])
def get_appointments():
    return jsonify(list(db.appointments.values()))


@app.route('/api/appointments/<int:appointment_id>/', methods=['GET'])
def get_appointment(appointment_id):
    appointment = db.appointments.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(appointment)


@app.route('/api/appointments/<int:appointment_id>/cancel/', methods=['PUT'])
def cancel_appointment(appointment_id):
    appointment = db.appointments.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404
    
    appointment['status'] = "cancelled"
    return jsonify({"message": "Appointment cancelled", "appointment": appointment})


@app.route('/api/appointments/<int:appointment_id>/', methods=['DELETE'])
def delete_appointment(appointment_id):
    if appointment_id not in db.appointments:
        return jsonify({"error": "Appointment not found"}), 404
    
    del db.appointments[appointment_id]
    return jsonify({"message": "Appointment deleted"})


# ==============================
# --- Main ---
# ==============================

if __name__ == '__main__':
    app.run(debug=True)
