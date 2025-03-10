from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    mobile_no = fields.CharField(max_length=20, unique=True, null=True)
    password = fields.CharField(max_length=100, null=True)
    images = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class RoleMaster(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    description = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_by = fields.IntField(null=True)

class RoleMapping(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="user_role_mappings", on_delete=fields.CASCADE)
    role = fields.ForeignKeyField("models.RoleMaster", related_name="role_mappings", on_delete=fields.CASCADE)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.IntField(null=True)  
    modified_at = fields.DatetimeField(auto_now=True)
    modified_by = fields.IntField(null=True) 