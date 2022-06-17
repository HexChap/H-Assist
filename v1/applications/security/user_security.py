from datetime import timedelta, datetime
from typing import Union, Optional

from jose import jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from v1.core.config import settings


SECRET_KEY, ALGORITHM = settings.security_settings.SECRET_KEY, settings.security_settings.ALGORITHM
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def authenticate_user(user, password: str):
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=60*60))
    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY)


class OAuth2PasswordBearerCookies(OAuth2PasswordBearer):
    def __call__(self, request: Request) -> Optional[str]:
        if not (authorization := request.headers.get("Authorization")):
            authorization: str = request.cookies.get("Authorization")

        scheme, _, token = authorization.partition(" ")

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return token
