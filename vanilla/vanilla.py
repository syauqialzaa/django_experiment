from fastapi import FastAPI
import uvicorn
import authentication, service_management, appointment
from database import get_db_connection

# Initialize
app = FastAPI(
    title="KHealthLinkr API",
    description="API manajemen appointment untuk health services."
)

# Include Router
app.include_router(authentication.router)
app.include_router(service_management.router)
app.include_router(appointment.router)

def check_db_connection():
    """
    Check database connection on startup.
    """
    try:
        conn = get_db_connection()
        if conn:
            print("Successfully connected to the PostgreSQL database.")
            conn.close()
        else:
            print("Failed to connect to the PostgreSQL database.")
    except Exception as e:
        print(f"Error during database startup check: {e}")


# app = FastAPI(lifespan=check_db_connection)
check_db_connection()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Clinic Management API"}

if __name__ == "__main__":
    uvicorn.run("vanilla:app", host="0.0.0.0", port=8000, reload=True)