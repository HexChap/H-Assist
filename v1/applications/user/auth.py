from datetime import timedelta, datetime
from typing import Union

from jose import jwt
from passlib.context import CryptContext

from v1.core import settings, errors

SECRET_KEY, ALGORITHM = settings.security.secret_key,\
                        settings.security.algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def authenticate_user(user, password: str):
    if not verify_password(password, user.password_hash):
        raise errors.IncorrectPassword
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=60*60))
    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY)
