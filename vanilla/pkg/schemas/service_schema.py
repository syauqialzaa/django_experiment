from pydantic import BaseModel
from uuid import UUID
from typing import List
from datetime import datetime

class ServiceCreatePayload(BaseModel):
  facility_name: str
  service_name: str
  list_doctor: List[str]

class ServiceUpdatePayload(BaseModel):
  facility_name: str
  service_name: str
  list_doctor: List[str]

class ServiceData(BaseModel):
  id: UUID
  service_name: str
  facility_name: str
  list_doctor: List[str]
  created_at: datetime

  class Config:
    from_attributes= True

class GetAllServiceResponse(BaseModel):
  status: str
  message: str
  data: List[ServiceData] 

class ServiceResponse(BaseModel):
  status: str
  message: str
  data: ServiceData 