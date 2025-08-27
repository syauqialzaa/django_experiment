from fastapi import APIRouter, HTTPException, status
from psycopg.rows import dict_row
from database import get_db_connection
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import models

# Brief 1 - Authentication & Authorization API
router = APIRouter(prefix="/api")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# GET /api/login/
@router.post("/login/")
def login_for_access_token(user: models.UserLogin):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=dict_row) as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (user.username,))
            db_user = cur.fetchone()

            if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
            access_token = create_access_token(data={"sub": db_user["username"], "role": db_user["role"]})
            return {"access_token": access_token, "token_type": "bearer"}
    finally:
        conn.close()

# POST /api/signup/
@router.post("/signup/", status_code=status.HTTP_201_CREATED, response_model=models.UserResponse)
def signup(user: models.UserCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=dict_row) as cur:
            # Check username
            cur.execute("SELECT 1 FROM users WHERE username = %s", (user.username,))
            if cur.fetchone():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
            
            hashed_password = pwd_context.hash(user.password)
            cur.execute(
                "INSERT INTO users (username, email, hashed_password, role) VALUES (%s, %s, %s, %s) RETURNING id, username, email, role",
                (user.username, user.email, hashed_password, user.role.value)
            )
            new_user = cur.fetchone()
            conn.commit()
            return new_user
    finally:
        conn.close()
        
# GET /api/user/{user_id}/
@router.get("/user/{user_id}/", response_model=models.UserResponse)
def get_user_by_id(user_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    try:
        with conn.cursor(cursor_factory=dict_row) as cur:
            cur.execute("SELECT id, username, email, role FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    finally:
        conn.close()
        
# PUT /api/user/{user_id}/update
@router.put("/user/{user_id}/update", response_model=models.GenericResponse)
def update_user(user_id: int, user: models.UserCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="User not found")
            
            hashed_password = pwd_context.hash(user.password)
            cur.execute(
                "UPDATE users SET username = %s, email = %s, hashed_password = %s, role = %s WHERE id = %s",
                (user.username, user.email, hashed_password, user.role.value, user_id)
            )
            conn.commit()
            return {"status": True, "message": "User updated successfully"}
    finally:
        conn.close()

# DELETE /api/user/{user_id}/update
@router.delete("/user/{user_id}/update", response_model=models.GenericResponse)
def delete_user(user_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="User not found")
            
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return {"status": True, "message": "User deleted successfully"}
    finally:
        conn.close()