from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    administrator = "administrator"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.patient

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ServiceCreate(BaseModel):
    name: str
    clinic_name: str
    doctor_id: int

class ServiceResponse(BaseModel):
    id: int
    name: str
    clinic_name: str
    doctor_id: int
    doctor_name: str

class AppointmentCreate(BaseModel):
    patient_id: int
    service_id: int
    appointment_time: datetime
    
class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    patient_name: str
    service_id: int
    service_name: str
    appointment_time: datetime
    status: str
    
class GenericResponse(BaseModel):
    status: bool
    message: str