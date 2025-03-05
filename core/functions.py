import jwt
import uuid
from datetime import datetime, timedelta
from calendar import timegm

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from core.database import get_db
from apps.users.models import User, RoleMapping

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  

def jwt_payload_handler(user, db: Session):
    """
    Generate a custom JWT payload, including user roles.
    """
    if user.last_login_role is None:
        role_mapping = db.query(RoleMapping).filter(RoleMapping.user_id == user.id).order_by(RoleMapping.created_at).first()
        role_name = role_mapping.role_obj.name if role_mapping and role_mapping.role_obj else "customer"
    else:
        role_name = user.last_login_role

    payload = {
        "user_id": user.id,
        "email": user.email,
        "user_role": role_name,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
    }

    return payload

def jwt_encode_handler(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def jwt_decode_handler(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def jwt_get_userid_from_payload(payload):
    return payload.get("user_id", None)

def generate_jwt_token(user, db):
    payload = jwt_payload_handler(user, db)
    return jwt_encode_handler(payload)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
