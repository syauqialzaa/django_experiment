import hashlib
from datetime import datetime

class DataStore:
    def __init__(self):
        self.users = {}
        self.services = {}
        self.appointments = {}
        self._id_counters = {'user': 1, 'service': 1, 'appointment': 1}

    def _get_next_id(self, entity):
        id_val = self._id_counters[entity]
        self._id_counters[entity] += 1
        return id_val

    # --- User Methods ---
    def create_user(self, data):
        user_id = self._get_next_id('user')
        hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
        # Ensure 'doctor' role can be set during creation
        self.users[user_id] = {
            'id': user_id,
            'username': data['username'],
            'email': data['email'],
            'password_hash': hashed_password,
            'role': data.get('role', 'patient') # Default role is 'patient'
        }
        return self.users[user_id]

    def find_user_by_username(self, username):
        for user in self.users.values():
            if user['username'] == username:
                return user
        return None
        
    def find_user_by_id(self, user_id):
        return self.users.get(user_id)

    # --- Service Methods (DILENGKAPI) ---
    def create_service(self, data):
        """Creates a new service."""
        service_id = self._get_next_id('service')
        doctor = self.find_user_by_id(data['doctor_id'])
        if not doctor or doctor['role'] != 'doctor':
            return None # Doctor not found or user is not a doctor
            
        self.services[service_id] = {
            'id': service_id,
            'name': data['name'],
            'clinic_name': data['clinic_name'],
            'doctor_id': data['doctor_id']
        }
        return self.services[service_id]

    def list_services(self):
        """Returns a list of all services."""
        return list(self.services.values())

    def find_service_by_id(self, service_id):
        """Finds a single service by its ID."""
        return self.services.get(service_id)

    # --- Appointment Methods (DILENGKAPI) ---
    def create_appointment(self, data):
        """Creates a new appointment."""
        appointment_id = self._get_next_id('appointment')
        
        # Validate user and service existence
        if not self.find_user_by_id(data['user_id']) or not self.find_service_by_id(data['service_id']):
            return None

        self.appointments[appointment_id] = {
            'id': appointment_id,
            'user_id': data['user_id'],
            'service_id': data['service_id'],
            'appointment_date': data['appointment_date'],
            'status': 'booked', # Default status
            'created_at': datetime.utcnow().isoformat()
        }
        return self.appointments[appointment_id]

    def get_user_appointments(self, user_id):
        """Returns all appointments for a specific user."""
        user_apps = []
        for app in self.appointments.values():
            if app['user_id'] == user_id:
                user_apps.append(app)
        return user_apps

# Create a single instance to act as our in-memory database
db = DataStore()# not an important file, you can delete this file