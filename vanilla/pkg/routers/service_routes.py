from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from vanilla.pkg.database.database import get_db
from vanilla.pkg.schemas.service_schema import ServiceResponse, ServiceCreatePayload, GetAllServiceResponse, ServiceUpdatePayload
from vanilla.pkg.controller import service_controller

router = APIRouter()

@router.post("/api/services", tags=["services"], status_code=status.HTTP_201_CREATED, response_model=ServiceResponse)
async def create_service(service_create_payload: ServiceCreatePayload, db: Session = Depends(get_db)):
  return service_controller.service_create(service_create_payload, db)

@router.get("/api/services", tags=["services"], status_code=status.HTTP_200_OK, response_model=GetAllServiceResponse)
async def get_all_services(db: Session = Depends(get_db)):
  return service_controller.get_all_services(db)

@router.get("/api/services/{service_id}", tags=["services"], status_code=status.HTTP_200_OK, response_model=ServiceResponse)
async def get_service(service_id: str, db: Session = Depends(get_db)):
  return service_controller.get_service(db, service_id)

@router.put("/api/services/{service_id}", tags=["services"], status_code=status.HTTP_200_OK, response_model=ServiceResponse)
async def get_service(service_id: str, update_service_payload: ServiceUpdatePayload, db: Session = Depends(get_db)):
  return service_controller.update_service(db, service_id, update_service_payload)

@router.delete("/api/services/{service_id}", tags=["services"], status_code=status.HTTP_200_OK, response_model=ServiceResponse)
async def delete_service(service_id: str, db: Session = Depends(get_db)):
  return service_controller.delete_service(db, service_id)