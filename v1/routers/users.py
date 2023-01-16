from fastapi import APIRouter, HTTPException, status, Request

from v1.applications.user import schemas, UserCRUD
from v1.core import errors

__tags__ = ["user"]
__prefix__ = "/users"

router = APIRouter()


@router.get("/", response_model=list[schemas.UserResponse])
async def get_users(request: Request):
    return await UserCRUD.get_all()


@router.post("/", response_model=schemas.UserResponse)
async def create_user(payload: schemas.UserPayload):
    """
    Creating user in the database. Payload must contains **username**, **email** and **password**

    :param payload: Payload for user.
    :return: None
    """
    try:
        return await UserCRUD.create(payload)
    except errors.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже существует."
        )
