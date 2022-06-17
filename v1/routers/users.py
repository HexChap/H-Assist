from typing import Union

from fastapi import APIRouter, HTTPException, Body, Depends, status

from v1.core.dependencies import (get_current_active_superuser,
                                  get_current_active_user)
from v1.applications.user import models, schemas, UserCRUD

__tags__ = ["users"]
__prefix__ = "/api/v1/users"

router = APIRouter()
users = UserCRUD()


@router.get("/")
async def get_users() -> list[models.User]:
    return await users.get_all()


@router.get("/{data}")
async def get_user_by_username(data: Union[int, str]) -> models.User:
    if isinstance(data, int):
        return await users.get_by_id(data)

    return await users.get_by_username(data)


@router.post("/")
async def create_user(
    *,
    user_payload: schemas.UserCreate,
    _ = Depends(get_current_active_superuser)
) -> models.User:
    if await users.get_by_email(user_payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists."
        )

    return await users.create(user_payload)


@router.put("/")
async def update_user(
    password: str = Body(None),
    r_password: str = Body(None),
    username: str = Body(None),
    email: str = Body(None),
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    user_in = schemas.UserUpdate(**dict(current_user))

    if password:
        user_in.password = password
        user_in.repeated_password = r_password
    if username:
        user_in.username = username
    if email:
        user_in.email = email

    return await users.update(current_user, user_in)
