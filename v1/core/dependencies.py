from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from v1.core import settings
from v1.applications.user import UserCRUD, models


class OAuth2PasswordBearerCookies(OAuth2PasswordBearer):
    def __call__(self, request: Request) -> str | None:
        exc = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not (authorization := request.headers.get("Authorization")):
            if not (authorization := request.cookies.get("Authorization")):
                raise exc

        scheme, _, token = authorization.partition(" ")

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise exc
            else:
                return None
        return token


oauth2_scheme = OAuth2PasswordBearerCookies(tokenUrl="token")
SECRET_KEY, ALGORITHM = settings.security.secret_key,\
                        settings.security.algorithm


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if not (user := await UserCRUD.get_by_email(email)):
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: models.UserORM = Depends(get_current_user)
) -> models.UserORM:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user."
        )

    return current_user


# async def get_current_active_superuser(
#     current_user: models.UserORM = Depends(get_current_active_user)
# ) -> models.UserORM:
#     if not current_user.is_superuser:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="The user does not have enough privileges."
#         )
#
#     return current_user
