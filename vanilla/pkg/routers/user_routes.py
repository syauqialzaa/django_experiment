from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from vanilla.pkg.database.database import get_db
from vanilla.pkg.controller import user_controller
from vanilla.pkg.schemas.user_schema import UserCreate, UserResponse, UserLoginResponse, UserLogin

router = APIRouter()

@router.get("/get-message", tags=["users"])
async def read_get_message():
  return {"message": "get your message"}

@router.post("/api/signup", tags=["users"], status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
  return user_controller.create_user(db=db, user=user)

@router.post("/api/login", tags=["users"], status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
async def user_login(login_payload: UserLogin, db:Session = Depends(get_db)):
  return user_controller.user_login(db=db, login_payload=login_payload)
