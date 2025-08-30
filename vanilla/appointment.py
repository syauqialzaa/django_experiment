from fastapi import APIRouter, HTTPException, status
from psycopg.rows import dict_row
from database import get_db_connection
import models

# Brief 3 endpoints for booking, cancelling, and viewing appointments.
router = APIRouter(prefix="/api", tags=["Appointments"])

# POST /api/appointments/book/
@router.post("/appointments/book/", status_code=status.HTTP_201_CREATED, response_model=models.GenericResponse)
def book_appointment(appointment: models.AppointmentCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO appointments (patient_id, service_id, appointment_time, status) VALUES (%s, %s, %s, %s)",
                (appointment.patient_id, appointment.service_id, appointment.appointment_time, "booked")
            )
            conn.commit()
            return {"status": True, "message": "Appointment booked successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# POST /api/appointments/{appointment_id}/cancel/
@router.post("/appointments/{appointment_id}/cancel/", status_code=status.HTTP_200_OK, response_model=models.GenericResponse)
def cancel_appointment(appointment_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE appointments SET status = 'cancelled' WHERE id = %s",
                (appointment_id,)
            )
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Appointment not found")
            
            conn.commit()
            return {"status": True, "message": "Appointment cancelled successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# GET /api/appointments/
@router.get("/appointments/", response_model=list[models.AppointmentResponse])
def get_all_appointments():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=dict_row) as cur:
            cur.execute("""
                        SELECT id, patient_id, users.username as patient_name, service_id, services.name as service_name, appointment_time, status FROM appointments
                        JOIN users ON appointments.patient_id = users.id
                        JOIN services ON appointments.service_id = services.id
                        ORDER BY appointment_time DESC
                    """)
            appointments = cur.fetchall()
            return appointments
    finally:
        conn.close()