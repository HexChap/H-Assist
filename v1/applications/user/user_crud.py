from typing import Optional
from datetime import datetime

from tortoise.exceptions import DoesNotExist

from v1.applications.security import hash_password
from . import schemas, models

KEYS_TO_DEL = {"id", "password", "repeated_password"}


class UserCRUD:
    def __init__(self):
        self.user_model_orm = models.User

    async def get_all(self) -> list[models.User]:
        return await self.user_model_orm.all()

    async def get_by_id(self, id: int) -> Optional[models.User]:
        try:
            return await self.user_model_orm.get(id=id)
        except DoesNotExist:
            return None

    async def get_by_email(self, email) -> Optional[models.User]:
        try:
            return await self.user_model_orm.get(email=email)
        except DoesNotExist:
            return None

    async def get_by_username(self, username) -> Optional[models.User]:
        try:
            return await self.user_model_orm.get(username=username)
        except DoesNotExist:
            return None

    async def create(self, user_payload: schemas.UserCreate) -> models.User:
        password_hash = hash_password(password=user_payload.password)
        user_payload = user_payload.dict()

        return await self.user_model_orm.create(**user_payload, password_hash=password_hash)

    async def update(self, to_update: models.User, user_payload: schemas.UserUpdate):
        payload = user_payload.dict()
        payload.update(updated_at=datetime.utcnow())

        return await to_update.update_from_dict(payload).save()
