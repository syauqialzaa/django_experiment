from .models import User, Service, Appointment

def user_to_dict(user: User) -> dict:
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }

def service_to_dict(service: Service) -> dict:
    return {
        'id': service.id,
        'name': service.name,
        'clinic_name': service.clinic_name,
        'doctor': user_to_dict(service.doctor)
    }

# DITAMBAHKAN untuk konsistensi
def appointment_to_dict(appointment: Appointment) -> dict:
    return {
        'id': appointment.id,
        'user': user_to_dict(appointment.user),
        'service': service_to_dict(appointment.service),
        'appointment_date': appointment.appointment_date,
        'status': appointment.status
    }