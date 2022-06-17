from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from v1.core.config import settings
from v1.applications.user import UserCRUD, models
from v1.applications.security import OAuth2PasswordBearerCookies

users = UserCRUD()
oauth2_scheme = OAuth2PasswordBearerCookies(tokenUrl="token")
SECRET_KEY, ALGORITHM = settings.security_settings.SECRET_KEY,\
                        settings.security_settings.ALGORITHM


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

    if not (user := await users.get_by_email(email)):
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user."
        )

    return current_user


async def get_current_active_superuser(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user does not have enough privileges."
        )

    return current_user
