from datetime import timedelta

from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from v1.applications.user import UserCRUD, auth, schemas
from v1.core.dependencies import get_current_active_user
from v1.core import settings, errors

__tags__ = ["auth"]
__prefix__ = ""

router = APIRouter()


@router.post("/auth", response_model=schemas.TokenResponse)
async def login_for_token(*, form_data: schemas.CredentialsRequest):
    if not (user := await UserCRUD.get_by_email(form_data.email)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The user with this email could not be found"
        )

    try:
        user = auth.authenticate_user(user, form_data.password)
    except errors.IncorrectPassword:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The password is incorrect"
        )

    access_token_expires = timedelta(
        minutes=settings.security.access_token_expire_minutes
    )
    token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    resp = JSONResponse({"access_token": token, "token_type": "bearer"})
    resp.set_cookie(
        "Authorization",
        f"Bearer {token}",
        expires=settings.security.access_token_expire_minutes,
        httponly=True
    )

    return resp


@router.get("/logout")
async def logout(
        response: Response,
        _=Depends(get_current_active_user)
):
    response = JSONResponse({"message": "Logout successful"})
    response.delete_cookie(key="Authorization")

    return response
