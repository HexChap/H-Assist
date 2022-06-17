from tortoise.fields import CharField, BooleanField

from v1.core.bases.models import AbstractBaseModel
from v1.validtors import EmailValidator


class User(AbstractBaseModel):
    email = CharField(max_length=255, unique=True, validators=[EmailValidator()])
    username = CharField(max_length=16, unique=True)
    password_hash = CharField(max_length=128)
    is_active = BooleanField()
    is_superuser = BooleanField()

    class Meta:
        table = "users"
