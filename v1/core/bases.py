from tortoise import Model, fields


class AbstractModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
