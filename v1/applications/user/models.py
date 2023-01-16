import typing

from tortoise import fields

from v1.core.bases import AbstractModel

if typing.TYPE_CHECKING:
    from v1.applications.record.models import RecordORM


class UserORM(AbstractModel):
    username = fields.TextField()
    email = fields.TextField()
    password_hash = fields.TextField()
    is_active = fields.BooleanField()

    record: fields.ReverseRelation["RecordORM"]

    class Meta:
        table = "users"
