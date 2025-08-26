from repositories import user_repo, service_repo, appointment_repo
import hashlib

class AuthService:
    def register_user(self, username, email, password, role):
        if user_repo.find_by_username(username):
            raise ValueError("Username already exists")
        
        hashed_password = self._hash_password(password)
        new_user_data = {
            'username': username,
            'email': email,
            'password_hash': hashed_password,
            'role': role
        }
        return user_repo.save(new_user_data)

    def login_user(self, username, password):
        user = user_repo.find_by_username(username)
        if user and self._verify_password(password, user['password_hash']):
            return user
        return None

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, plain_password, hashed_password):
        return self._hash_password(plain_password) == hashed_password

class ServiceService:
    def create_service(self, name, clinic_name, doctor_id):
        """Creates a new medical service, ensuring the creator is a doctor."""
        doctor = user_repo.get(doctor_id)
        if not doctor:
            raise ValueError("Doctor user not found.")
        if doctor.get('role') != 'doctor':
            raise PermissionError("Only users with the 'doctor' role can create services.")
        
        new_service_data = {
            'name': name,
            'clinic_name': clinic_name,
            'doctor_id': doctor_id
        }
        return service_repo.save(new_service_data)

    def get_all_services(self):
        """Retrieves all services and includes doctor information."""
        services = service_repo.all()
        for service in services:
            doctor = user_repo.get(service['doctor_id'])
            service['doctor_info'] = {
                'id': doctor['id'],
                'username': doctor['username'],
                'email': doctor['email']
            } if doctor else None
        return services

class AppointmentService:
    def book_appointment(self, user_id, service_id, appointment_date):
        """Books an appointment, validating user and service existence."""
        user = user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found.")
            
        service = service_repo.get(service_id)
        if not service:
            raise ValueError(f"Service with id {service_id} not found.")

        new_appointment_data = {
            'user_id': user_id,
            'service_id': service_id,
            'appointment_date': appointment_date,
            'status': 'confirmed'
        }
        return appointment_repo.save(new_appointment_data)

    def get_appointments_for_user(self, user_id):
        """Retrieves all appointments for a specific user."""
        if not user_repo.get(user_id):
            raise ValueError(f"User with id {user_id} not found.")
        
        all_appointments = appointment_repo.all()
        user_appointments = [app for app in all_appointments if app['user_id'] == user_id]
        
        # Enhance with service details
        for app in user_appointments:
            service = service_repo.get(app['service_id'])
            app['service_info'] = service

        return user_appointments

# Instantiate services
auth_service = AuthService()
service_service = ServiceService() # ADDED
appointment_service = AppointmentService() # ADDED