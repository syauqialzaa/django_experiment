from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from vanilla.pkg.database.database import get_db
from vanilla.pkg.controller import user_controller
from vanilla.pkg.schemas.user_schema import UserCreate, UserResponse, UserLogin, EditUser

router = APIRouter()

@router.get("/get-message", tags=["users"])
async def read_get_message():
  return {"message": "get your message"}

@router.post("/api/signup", tags=["users"], status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
  return user_controller.create_user(db, user)

@router.post("/api/login", tags=["users"], status_code=status.HTTP_200_OK, response_model=UserResponse)
async def user_login(login_payload: UserLogin, db:Session = Depends(get_db)):
  return user_controller.user_login(db, login_payload)

@router.get("/api/users/{user_id}", tags=["users"], status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_data(user_id: str, db: Session = Depends(get_db)):
  return user_controller.get_user(db, user_id)

@router.put("/api/users/{user_id}", tags=["users"], status_code=status.HTTP_200_OK, response_model=UserResponse)
async def edit_user_data(user_id: str, edit_user_payload: EditUser, db: Session = Depends(get_db)):
  return user_controller.update_user(db, user_id, edit_user_payload)

@router.delete("/api/users/{user_id}", tags=["users"], status_code=status.HTTP_200_OK, response_model=UserResponse)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
  return user_controller.delete_user(db, user_id)