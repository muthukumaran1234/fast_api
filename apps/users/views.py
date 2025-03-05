import json
from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from . import models, schemas
from apps.users.models import RoleMaster
from apps.users.schemas import RoleCreate
from core.functions import hash_password, send_email
from sqlalchemy import case

def get_users(db: Session):
    users = db.query(models.User).all()
    user_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return Response(content=json.dumps({"status": "success", "message": "Users fetched successfully", "data": user_data}), status_code=200)


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user_data = {"id": user.id, "username": user.username, "email": user.email}
    return Response(content=json.dumps({"status": "success", "message": "User fetched successfully", "data": user_data}), status_code=200)


def create_user(db: Session, user: schemas.UserCreate):
    password = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password=password)
    send_email(user.email,"User request Mail",f"{user.username} created succssfully")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    role_names = user.roles if user.roles else ["customer"]
    #to ordering the roles 
    order_cases = [case((models.RoleMaster.name == name, index)) for index, name in enumerate(role_names)]
    roles = (db.query(models.RoleMaster).filter(models.RoleMaster.name.in_(role_names)).order_by(*order_cases).all())
    if not roles:
        raise HTTPException(status_code=400, detail="Invalid roles provided.")

    for role in roles:
        user_role = models.RoleMapping(user_id=db_user.id, role_id=role.id)
        db.add(user_role)

    db.commit()

    return Response(content=json.dumps({"status": "success", "message": "User created successfully"}), status_code=201)



def get_roles(db: Session):
    roles = db.query(RoleMaster).all()
    role_data = [{"id": role.id, "name": role.name, "description": role.description} for role in roles]
    return Response(content=json.dumps({"status": "success", "message": "Roles fetched successfully", "data": role_data}), status_code=200)


def create_role(db: Session, role: RoleCreate, current_user: str):
    if current_user != "admin":
        raise HTTPException(status_code=401, detail="You are not authenticated to perform this action")

    new_role = RoleMaster(name=role.name, description=role.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return Response(content=json.dumps({"status": "success", "message": "Role created successfully"}), status_code=201)


