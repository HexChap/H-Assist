from . import models, schemas


class RecordCRUD:
    record = models.RecordORM

    @classmethod
    async def get(cls, record_id):
        if not (record := await cls.record.get_or_none(id=record_id)):
            return "Does not exists."

        return record

    @classmethod
    async def get_all(cls):
        return await cls.record.all()

    @classmethod
    async def get_by_email(cls, email: str) -> list[record]:
        return await cls.record.filter(
            user=await cls.record.user.get(email=email)
        )

    @classmethod
    async def create(cls, payload: schemas.RecordPayload, user_id: int):
        """
        :param payload: Sign in/up payload
        :return: None
        """

        return await cls.record.create(**payload.dict(), user_id=user_id)
