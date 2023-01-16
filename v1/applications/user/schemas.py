import datetime

from pydantic import BaseModel, constr, EmailStr


class UserPayload(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8)


class CredentialsRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    password_hash: str
    is_active: str
    created_at: datetime.datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
