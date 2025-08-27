from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from vanilla.pkg.models.user_model import User
from vanilla.pkg.utils.hash import hash_password, verify_password
from vanilla.pkg.schemas.user_schema import UserCreate, UserResponse, UserLogin, UserLoginResponse, EditUser


def create_user(db: Session, user: UserCreate):
  try:
    # cek email
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already registered"
      )
    
    # cek username
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already registered"
      )

    hashedPassword = hash_password(user.password)
    
    new_user = User( 
        username=user.username,
        email=user.email,
        password=hashedPassword,
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        status="success",
        message="User created successfully",
        data=new_user
    )
  
  except HTTPException:  
    # biarkan HTTPException tetap dilempar keluar
    raise 
  
  except Exception as e:
    db.rollback()  # batalkan transaksi kalau error
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to create user: {str(e)}"
    )

def user_login(db: Session, login_payload: UserLogin):
  try:
    existing_user = db.query(User).filter(User.username == login_payload.username).first()
    if not existing_user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
      )

    is_password_match = verify_password(login_payload.password, existing_user.password)
    if not is_password_match:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong password"
      )
    
    return UserLoginResponse(
      message="User logged in successfully",
      status="success",
      data=existing_user
    )
  
  except HTTPException:  
    # biarkan HTTPException tetap dilempar keluar
    raise

  except Exception as e:
      db.rollback()  # batalkan transaksi kalau error
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Failed to login: {str(e)}"
      )

def get_user(db: Session, user_id: str):
  try:
     
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
      )
    
    return UserResponse(
      status="success",
      message="User fetched successfully",
      data=existing_user
    )
  
  except HTTPException:  
    # biarkan HTTPException tetap dilempar keluar
    raise

  except Exception as e:
      db.rollback()  # batalkan transaksi kalau error
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Failed to get user: {str(e)}"
      )

def update_user(db: Session, user_id: str, edit_user_payload: EditUser):
  try:
     
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
      )
    
    existing_user.role = edit_user_payload.role
    existing_user.password = edit_user_payload.password

    db.commit()
    db.refresh(existing_user)

    return UserResponse(
      status="success",
      message="User updated successfully",
      data=existing_user
    )
  
  except HTTPException:  
    # biarkan HTTPException tetap dilempar keluar
    raise

  except Exception as e:
      db.rollback()  # batalkan transaksi kalau error
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Failed to update user: {str(e)}"
      )
  
def delete_user(db: Session, user_id: str):
    try:
       
      existing_user = db.query(User).filter(User.id == user_id).first()
      if not existing_user:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="User not found"
          )

      db.delete(existing_user)
      db.commit()

      return UserResponse(
          status="success",
          message="User deleted successfully",
          data=existing_user
      )
    
    except HTTPException:  
      # biarkan HTTPException tetap dilempar keluar
      raise

    except Exception as e:
      db.rollback()  # batalkan transaksi kalau error
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Failed to delete user: {str(e)}"
      )