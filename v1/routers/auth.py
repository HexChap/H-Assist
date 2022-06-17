from datetime import timedelta

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from v1.applications.security import (authenticate_user, create_access_token,
                                      CustomPasswordRequestForm)
from v1.applications.user import UserCRUD
from v1.core.config import settings

__tags__ = ["auth"]
__prefix__ = "/api/v1/auth"

router = APIRouter()
users = UserCRUD()


@router.post("/token")
async def login_for_token(*, form_data: CustomPasswordRequestForm):
    if not (user := await users.get_by_email(form_data.email)):
        return "The user with this email could not be found."

    user = authenticate_user(user, form_data.password)
    access_token_expires = timedelta(
        minutes=settings.security_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    resp = JSONResponse({"access_token": token, "token_type": "bearer"})
    resp.set_cookie("Authorization", f"Bearer {token}", expires=access_token_expires)

    return resp

