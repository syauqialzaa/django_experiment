from flask import Blueprint, request, jsonify
from models import db
import hashlib

api_bp = Blueprint('api', __name__)

# --- Brief 1: Authentication & Authorization ---
@api_bp.route('/signup/', methods=['POST'])
def signup():
    data = request.json
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"error": "Missing required fields"}), 400
        
    if db.find_user_by_username(data['username']):
        return jsonify({"error": "Username already exists"}), 409 # 409 Conflict is more appropriate
    
    user = db.create_user(data)
    return jsonify({"message": "User created", "user_id": user['id']}), 201

@api_bp.route('/login/', methods=['POST']) # Changed to POST for security
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    username = data.get('username')
    password = data.get('password')
    
    user = db.find_user_by_username(username)
    if user and user['password_hash'] == hashlib.sha256(password.encode()).hexdigest():
        # In a real app, you would generate a token (e.g., JWT) here
        return jsonify({
            "message": "Login successful", 
            "user_id": user['id'],
            "role": user['role']
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

# --- Brief 2: Service Management (ENDPOINT BARU) ---
@api_bp.route('/services/', methods=['POST'])
def create_service():
    """Endpoint for doctors to create services."""
    data = request.json
    # Simple authorization: check if the user creating the service is a doctor
    # In a real app, this ID would come from a session token (e.g., JWT)
    creator_id = data.get('creator_id') 
    creator = db.find_user_by_id(creator_id)

    if not creator or creator['role'] != 'doctor':
        return jsonify({"error": "Unauthorized: Only doctors can create services"}), 403

    # The service must be linked to the doctor creating it
    service_data = {
        "name": data.get("name"),
        "clinic_name": data.get("clinic_name"),
        "doctor_id": creator_id
    }

    if not service_data['name'] or not service_data['clinic_name']:
        return jsonify({"error": "Missing service name or clinic name"}), 400

    service = db.create_service(service_data)
    return jsonify(service), 201

@api_bp.route('/services/', methods=['GET'])
def get_services():
    """Endpoint to list all available services."""
    services = db.list_services()
    # To make it more useful, let's include doctor info
    result = []
    for s in services:
        doctor = db.find_user_by_id(s['doctor_id'])
        s['doctor_name'] = doctor['username'] if doctor else 'Unknown'
        result.append(s)
    return jsonify(result), 200


# --- Brief 3: Appointment Booking (DILENGKAPI) ---
@api_bp.route('/appointments/book/', methods=['POST'])
def book_appointment():
    data = request.json
    required_fields = ['user_id', 'service_id', 'appointment_date']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields (user_id, service_id, appointment_date)"}), 400

    appointment = db.create_appointment(data)
    if not appointment:
        return jsonify({"error": "User or Service not found"}), 404

    return jsonify({"message": "Appointment booked successfully", "appointment": appointment}), 201

@api_bp.route('/users/<int:user_id>/appointments/', methods=['GET'])
def get_user_appointments(user_id):
    """Endpoint to get all appointments for a user."""
    user = db.find_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    appointments = db.get_user_appointments(user_id)
    return jsonify(appointments), 200