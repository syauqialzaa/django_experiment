from fastapi import APIRouter, status, Depends
from vanilla.pkg.schemas.appointments_schema import AppointmentResponse, AppointmentPayload, GetAllAppointmentResponse
from sqlalchemy.orm import Session
from vanilla.pkg.database.database import get_db
from vanilla.pkg.controller import appointments_controller

router = APIRouter()

@router.post("/api/appointments/book", tags=["appointments"], status_code=status.HTTP_201_CREATED, response_model=AppointmentResponse)
async def book_appointment(appointment_payload: AppointmentPayload,db: Session = Depends(get_db)):
  return appointments_controller.create_appointment(appointment_payload, db)

@router.post("/api/appointments/{appointment_id}/cancel", tags=["appointments"], status_code=status.HTTP_200_OK, response_model=AppointmentResponse)
async def cancel_book_appointment(appointment_id: str, db: Session = Depends(get_db)):
  return appointments_controller.cancel_appointment(appointment_id, db)

@router.get("/api/appointments", tags=["appointments"], status_code=status.HTTP_200_OK, response_model=GetAllAppointmentResponse)
async def get_all_appointments(db: Session = Depends(get_db)):
  return appointments_controller.get_all_appointments(db)
