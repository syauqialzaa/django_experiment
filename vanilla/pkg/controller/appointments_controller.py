from sqlalchemy.orm import Session
from vanilla.pkg.schemas.appointments_schema import AppointmentPayload, AppointmentResponse, GetAllAppointmentResponse
from vanilla.pkg.models.appointments_model import Appointment, AppointmentStatus
from fastapi import HTTPException, status


def create_appointment(appointment_payload: AppointmentPayload, db: Session):
  try:
    new_appointment = Appointment(
      patient_id = appointment_payload.patient_id,
      doctor_id = appointment_payload.doctor_id,
      service_id = appointment_payload.service_id,
      appointment_time = appointment_payload.appointment_time,
      status = appointment_payload.status,
      notes = appointment_payload.notes
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return AppointmentResponse(
      status="success",
      message="Appointment created successfully",
      data=new_appointment
    )

  except Exception as e:
    db.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Failed to create appointment: {str(e)}"
    )

def cancel_appointment(appointment_id: str, db: Session):
  try:
    existing_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not existing_appointment:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Appointment not found"
      )
    
    existing_appointment.status = AppointmentStatus.cancelled

    db.commit()
    db.refresh(existing_appointment)

    return AppointmentResponse(
      status="success",
      message="Appointment cancelled successfully",
      data=existing_appointment
    )
  
  except HTTPException:
    raise

  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Failed to cancel appointment: {str(e)}"
    )
  

def get_all_appointments(db: Session):
  try:
    all_appointments = db.query(Appointment).all()

    if not all_appointments:
      return GetAllAppointmentResponse(
        status="success",
        message="Appointments fetched successfully",
        data=[]
      )
    
    return GetAllAppointmentResponse(
      status="success",
      message="Appointments fetched successfully",
      data=all_appointments
    )
  
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Failed to fetch appointments: {str(e)}"
    )