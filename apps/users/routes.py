from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from core.database import get_db
from apps.users import views
from apps.users.schemas import RoleCreate, RoleResponse,UserCreate,UserResponse,TokenResponse,RefreshTokenRequest
from typing import List
from apps.users.models import User,RoleMaster,RoleMapping
from core.functions import generate_jwt_token, get_current_user, verify_password,jwt_encode_handler
from datetime import datetime, timedelta
router = APIRouter()


@router.get("/roles", response_model=List[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return views.get_roles(db)

@router.post("/roles", response_model=RoleResponse,)

def create_role(role: RoleCreate, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    print('routes---->>>>>>>>>>')
    return views.create_role(db, role,current_user)

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


@router.post("/refresh-token/")
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    user_id = request.userid
    user_role = request.change_role

    user_obj = db.query(User).filter(User.id == user_id).first()
    if not user_obj:
        raise HTTPException(status_code=400, detail="User ID does not exist.")
    #ilike->is used for case-sensitive
    role = db.query(RoleMaster).filter(RoleMaster.name.ilike(user_role), RoleMaster.is_active == True).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist or is inactive.")

    user_obj.last_login_role = user_role
    db.commit()

    role_list = [user_role]  
    role_mappings = db.query(RoleMapping).filter(RoleMapping.user_id == user_obj.id, RoleMapping.role_id == role.id).order_by(RoleMapping.role_id).all()
    
    for obj in role_mappings:
        role_name = db.query(RoleMaster.name).filter(RoleMaster.id == obj.role_id).scalar()
        if role_name and role_name not in role_list:
            role_list.append(role_name)

    payload = {
        "user_id": user_obj.id,
        "user_email": user_obj.email,
        "user_role": user_role,
        "exp": datetime.utcnow() + timedelta(hours=1)  
    }

    token = jwt_encode_handler(payload)

    return {"status": "success", "message": "Role changed successfully", "data": token}