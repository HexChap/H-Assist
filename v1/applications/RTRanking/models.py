from tortoise.fields import (
                            IntField, TextField, BooleanField,
                            ForeignKeyField, ForeignKeyRelation,
                            ManyToManyRelation, ManyToManyField
                            )

from v1.core.bases.models import AbstractBaseModel
from v1.applications.user.models import User


class Race(AbstractBaseModel):
    name = TextField()
    competitors: ManyToManyRelation["Competitor"] = ManyToManyField(
        "models.Competitor"
    )

    class Meta:
        table = "races"


class Competitor(AbstractBaseModel):
    added_by: ForeignKeyRelation[User] = ForeignKeyField(
        "models.User", "competitors"
    )
    name = TextField()
    start_number = IntField()
    is_highlighted = BooleanField()

    races: ManyToManyRelation[Race]

    class Meta:
        table = "competitors"
