from pydantic import BaseModel
from datetime import datetime
from vanilla.pkg.models.appointments_model import AppointmentStatus
from uuid import UUID
from typing import List

class AppointmentData(BaseModel):
  patient_id: UUID
  doctor_id: UUID
  service_id: UUID
  appointment_time: datetime
  status: AppointmentStatus
  notes: str

  class Config:
    from_attributes= True
  
class AppointmentPayload(BaseModel):
  patient_id: UUID
  doctor_id: UUID
  service_id: UUID
  appointment_time: datetime
  status: AppointmentStatus
  notes: str
  
class AppointmentResponse(BaseModel):
  status: str
  message: str
  data: AppointmentData

class GetAllAppointmentResponse(BaseModel):
  status: str
  message: str
  data: List[AppointmentData] 
