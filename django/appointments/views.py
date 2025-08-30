from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Appointment
from django.contrib.auth.models import User
from services.models import Service
import json

@csrf_exempt
@require_http_methods(["POST"])
def book_appointment(request):
    """
    API endpoint for patients to book appointments.
    POST /api/appointments/book/
    """
    try:
        data = json.loads(request.body)
        patient_id = data.get('patient_id')
        service_id = data.get('service_id')
        appointment_time = data.get('appointment_time')

        if not all([patient_id, service_id, appointment_time]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        patient = get_object_or_404(User, id=patient_id)
        service = get_object_or_404(Service, id=service_id)
        appointment = Appointment.objects.create(
            patient_id=patient_id,
            patient=patient,
            service=service,
            service_id=service_id,
            appointment_time=appointment_time,
            status='booked'
        )

        return JsonResponse({
            "message": "Appointment booked successfully",
            "appointment_id": appointment.id
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def cancel_appointment(request, appointment_id):
    """
    API endpoint for canceling an appointment.
    POST /api/appointments/{appointment_id}/cancel/
    """
    try:
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Check if the appointment can be canceled (e.g., not already canceled)
        if appointment.status == 'canceled':
            return JsonResponse({"message": "Appointment is already canceled."}, status=200)

        # Change the appointment status
        appointment.status = 'canceled'
        appointment.save()

        return JsonResponse({"message": "Appointment canceled successfully."}, status=200)

    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appointment not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["GET"])
def list_appointments(request):
    """
    API endpoint to display all appointments.
    GET /api/appointments/
    """
    appointments = Appointment.objects.all().select_related('patient', 'doctor_schedule__doctor')
    data = []
    for appointment in appointments:
        data.append({
            "id": appointment.id,
            "patient": appointment.patient.username,
            "doctor": appointment.service.doctors.first().username if appointment.service.doctors.exists() else None,
            "service": appointment.service.name,
            "date": appointment.appointment_time.date(),
            "status": appointment.status
        })
    return JsonResponse(data, safe=False)