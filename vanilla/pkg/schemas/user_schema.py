from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
  username: str
  email: EmailStr
  role: str
  password: str

class UserLogin(BaseModel):
  username: str
  password: str

class UserData(BaseModel):
  id: UUID
  username: str
  email: EmailStr
  role: str
  created_at: datetime
  password: str

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