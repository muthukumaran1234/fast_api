from fastapi import APIRouter
from .models import *
from .schemas import *
router = APIRouter()

@router.post("/role_create/",response_model=RoleMaster_Pydantic)
async def create_role(role: RoleMasterIn_Pydantic):
    role_obj = await RoleMaster.create(**role.dict())
    return await RoleMaster_Pydantic.from_tortoise_orm(role_obj)
