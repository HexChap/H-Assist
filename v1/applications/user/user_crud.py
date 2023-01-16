from . import models, schemas, auth
from v1.core import errors


class UserCRUD:
    user = models.UserORM

    @classmethod
    async def get_all(cls):
        return await cls.user.all()

    @classmethod
    async def get_by_email(cls, email: str):
        return await cls.user.get(email=email)

    @classmethod
    async def create(cls, payload: schemas.UserPayload):
        """
        :param payload: Sign in/up payload
        :return: None
        """
        p_hash = auth.hash_password(payload.password)

        if await cls.user.filter(email=payload.email) or await cls.user.filter(username=payload.username):
            raise errors.UserAlreadyExists

        return await cls.user.create(**payload.dict(), password_hash=p_hash, is_active=True)
