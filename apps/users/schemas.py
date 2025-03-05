from pydantic import BaseModel
from typing import Optional,List
class UserCreate(BaseModel):#post
    username: str
    email: str
    password: str
    roles: Optional[List[str]] = []  

class UserResponse(UserCreate):#get
    id: int
    username: str
    email: str

    # class Config:
    #     orm_mode = True



class TokenResponse(BaseModel):
    status: str
    message: str
    token: str


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(RoleCreate):
    id: int
