from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    last_login_role = Column(String, nullable=True)

    role_mappings = relationship("RoleMapping", back_populates="user_obj")

class RoleMaster(Base):
    __tablename__ = "role_master"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    modified_by = Column(Integer, nullable=True)

    role_mappings = relationship("RoleMapping", back_populates="role_obj")

class RoleMapping(Base):
    __tablename__ = "role_mapping"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role_master.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    modified_by = Column(Integer, nullable=True)

    user_obj = relationship("User", back_populates="role_mappings")
    role_obj = relationship("RoleMaster", back_populates="role_mappings")
