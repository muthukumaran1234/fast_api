from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    mobile_no = fields.CharField(max_length=20, unique=True, null=True)
    password = fields.CharField(max_length=100, null=True)