from flask import Blueprint, request, jsonify
# Updated imports to include the new services
from services import auth_service, service_service, appointment_service

api_bp = Blueprint('api', __name__)

@api_bp.route('/signup/', methods=['POST'])
def signup():
    try:
        data = request.json
        user = auth_service.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'patient')
        )
        return jsonify({"message": "User created", "user_id": user['id']}), 201
    except ValueError as e:
        # Use 409 Conflict for "already exists" errors
        return jsonify({"error": str(e)}), 409
    except Exception:
        return jsonify({"error": "An internal error occurred"}), 500

@api_bp.route('/login/', methods=['POST']) # Changed to POST
def login():
    try:
        data = request.json
        user = auth_service.login_user(data['username'], data['password'])
        if user:
            return jsonify({"message": "Login successful", "user_id": user['id'], "role": user['role']})
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception:
        return jsonify({"error": "An internal error occurred"}), 500

@api_bp.route('/services/', methods=['POST'])
def create_service():
    """Endpoint to create a new medical service."""
    try:
        data = request.json
        service = service_service.create_service(
            name=data['name'],
            clinic_name=data['clinic_name'],
            doctor_id=data['doctor_id'] # In a real app, this would come from a auth token
        )
        return jsonify(service), 201
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403 # Forbidden
    except ValueError as e:
        return jsonify({"error": str(e)}), 400 # Bad Request
    except Exception as e:
        return jsonify({"error": f"An internal error occurred: {e}"}), 500

@api_bp.route('/services/', methods=['GET'])
def list_services():
    """Endpoint to list all available medical services."""
    try:
        services = service_service.get_all_services()
        return jsonify(services)
    except Exception:
        return jsonify({"error": "An internal error occurred"}), 500

@api_bp.route('/appointments/book/', methods=['POST'])
def book_appointment():
    """Endpoint for users to book an appointment."""
    try:
        data = request.json
        appointment = appointment_service.book_appointment(
            user_id=data['user_id'],
            service_id=data['service_id'],
            appointment_date=data['appointment_date']
        )
        return jsonify({"message": "Appointment booked successfully", "appointment": appointment}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 # Not Found
    except Exception:
        return jsonify({"error": "An internal error occurred"}), 500

@api_bp.route('/users/<int:user_id>/appointments/', methods=['GET'])
def get_user_appointments(user_id):
    """Endpoint to get all appointments for a specific user."""
    try:
        appointments = appointment_service.get_appointments_for_user(user_id)
        return jsonify(appointments)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "An internal error occurred"}), 500