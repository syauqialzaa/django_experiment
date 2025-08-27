from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from vanilla.pkg.schemas.service_schema import ServiceCreatePayload
from vanilla.pkg.models.service_model import Service
from vanilla.pkg.schemas.service_schema import ServiceResponse, GetAllServiceResponse, ServiceUpdatePayload

def service_create(service_create_payload: ServiceCreatePayload, db: Session):
  try:
    new_service = Service(
      facility_name = service_create_payload.facility_name,
      list_doctor = service_create_payload.list_doctor
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return ServiceResponse(
      status="success",
      message="Service added successfully",
      data= new_service
    )
  
  except Exception as e:
    db.rollback()  # batalkan transaksi kalau error
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to create service: {str(e)}"
    )
  
def get_all_services(db: Session):
  try:
    all_service = db.query(Service).all()

    if not all_service:
      return GetAllServiceResponse(
        status="success",
        message="Services fetched successfully",
        data=[]
      )
    
    return GetAllServiceResponse(
      status="success",
      message="Services fetched successfully",
      data=all_service
    )
  
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Failed to fetch service: {str(e)}"
    )

def get_service(db: Session, service_id: str):
  try:
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Service not found"
      )
    
    return ServiceResponse(
      status="success",
      message="Service fetched successfully",
      data=service
    )
  
  except HTTPException:
    raise

  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Failed to fetch service: {str(e)}"
    )
  
def update_service(db: Session, service_id: str, update_service_payload: ServiceUpdatePayload):
  try:
    existing_service = db.query(Service).filter(Service.id == service_id).first()

    if not existing_service:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Service not found"
      )
    
    existing_service.facility_name = update_service_payload.facility_name
    existing_service.list_doctor = update_service_payload.list_doctor

    return ServiceResponse(
      status="success",
      message="Service updated successfully",
      data=existing_service
    )
  
  except HTTPException:
    raise

  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Failed to update service: {str(e)}"
    )
  
def delete_service(db: Session, service_id: str):
  try:
    existing_service = db.query(Service).filter(Service.id == service_id).first()

    if not existing_service:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Service not found"
      )
    
    db.delete(existing_service)
    db.commit()

    return ServiceResponse(
      status="success",
      message="Service deleted successfully",
      data=existing_service
    )
  
  except HTTPException:
    raise

  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Failed to delete service: {str(e)}"
    )