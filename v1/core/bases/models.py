from tortoise.fields import *
from tortoise import Model


class AbstractBaseModel(Model):
    id = IntField(pk=True)

    updated_at = DatetimeField(auto_now=True)
    created_at = DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
