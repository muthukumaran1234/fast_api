# from pydantic import BaseModel, EmailStr
# from typing import Optional, List

# class UserCreate(BaseModel):
#     name :str
#     email :EmailStr
#     mobile_no :str
#     password :str
#     images :Optional[List[str]] = []
    
# class UserResponse(BaseModel):
#     id :int
#     name :str
#     email :EmailStr
#     mobile_no :str
#     password :str
#     images :Optional[List[str]] = []
    
#     #below to allows orm modle conversion 
#     # class Config:
#     #     from_attributes = True
from tortoise.contrib.pydantic import pydantic_model_creator,pydantic_queryset_creator

from user.models import RoleMaster

RoleMaster_Pydantic = pydantic_model_creator(RoleMaster, name="RoleMaster_single_res")
RoleMaster_Pydantic_all = pydantic_queryset_creator(RoleMaster, name="RoleMaster_all_res")
RoleMasterIn_Pydantic = pydantic_model_creator(RoleMaster, name="RoleMasterCreate", exclude_readonly=True)