from fastapi import APIRouter, HTTPException, status
from psycopg.rows import dict_row
from database import get_db_connection
import models

# Brief 2 - Service Management
router = APIRouter(prefix="/api", tags=["Services"])

# GET /api/services/
@router.get("/services/", response_model=list[models.ServiceResponse])
def get_all_services():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=dict_row) as cur:
            cur.execute("""
                SELECT s.id, s.name, s.clinic_name, s.doctor_id, u.username as doctor_name
                FROM services s
                JOIN users u ON s.doctor_id = u.id
            """)
            services = cur.fetchall()
            return services
    finally:
        conn.close()
        
# POST /api/services/
@router.post("/services/", status_code=status.HTTP_201_CREATED, response_model=models.GenericResponse)
def add_service(service: models.ServiceCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO services (name, clinic_name, doctor_id) VALUES (%s, %s, %s)",
                (service.name, service.clinic_name, service.doctor_id)
            )
            conn.commit()
            return {"status": True, "message": "Service created successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
        
# GET /api/services/{service_id}/
@router.get("/services/{service_id}/", response_model=models.ServiceResponse)
def get_all_services():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=dict_row) as cur:
            cur.execute("""
                SELECT s.id, s.name, s.clinic_name, s.doctor_id, u.username as doctor_name
                FROM services s
                JOIN users u ON s.doctor_id = u.id
            """)
            services = cur.fetchall()
            return services
    finally:
        conn.close()

# PUT /api/services/{service_id}/
@router.put("/services/{service_id}/", response_model=models.GenericResponse)
def update_service(service_id: int, service: models.ServiceCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM services WHERE id = %s", (service_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Service not found")
            
            cur.execute(
                "UPDATE services SET name = %s, clinic_name = %s, doctor_id = %s WHERE id = %s",
                (service.name, service.clinic_name, service.doctor_id, service_id)
            )
            conn.commit()
            return {"status": True, "message": "Service updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# DELETE /api/services/{service_id}/
@router.delete("/services/{service_id}/", response_model=models.GenericResponse)
def delete_service(service_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM services WHERE id = %s", (service_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Service not found")
            
            cur.execute("DELETE FROM services WHERE id = %s", (service_id,))
            conn.commit()
            return {"status": True, "message": "Service deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()