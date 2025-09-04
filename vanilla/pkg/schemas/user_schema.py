from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
  patient = "patient"
  doctor = "doctor"
  administrator = "administrator"
  
class UserCreate(BaseModel):
  username: str
  email: EmailStr
  role: UserRole
  password: str

class UserLogin(BaseModel):
  username: str
  password: str

class EditUser(BaseModel):
  password: str
  role: UserRole

class UserData(BaseModel):
  id: UUID
  username: str
  email: EmailStr
  role: str
  created_at: datetime

  class Config:
    from_attributes= True

class UserResponse(BaseModel):
  status: str
  message: str
  data: UserData

class UserLoginResponse(BaseModel):
  status: str
  message: str
  data: UserData