from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from apps.users import views
from apps.users.schemas import RoleCreate, RoleResponse,UserCreate,UserResponse,TokenResponse
from typing import List
from apps.users.models import User
from core.functions import generate_jwt_token, verify_password

router = APIRouter()

@router.get("/roles", response_model=List[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return views.get_roles(db)

@router.post("/roles", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return views.create_role(db, role)

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return views.create_user(db,user)


@router.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return views.get_users(db)

@router.post("/login", response_model=TokenResponse)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    user = db.query(User).filter(User.email == email,User.is_active == True).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid mobile number or user not found.")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password.")

    token = generate_jwt_token(user, db)

    return {"status": "success", "message": "Login successful.", "token": token}
