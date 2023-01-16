import typing

from tortoise import fields

from v1.core.bases import AbstractModel

if typing.TYPE_CHECKING:
    from v1.applications.user.models import UserORM


class RecordORM(AbstractModel):
    title = fields.TextField()
    note = fields.TextField()

    user: fields.ForeignKeyRelation["UserORM"] = fields.ForeignKeyField(
        "models.UserORM", "records"
    )

    class Meta:
        table = "records"
