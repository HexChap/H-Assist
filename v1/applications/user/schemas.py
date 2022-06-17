from typing import Optional

from pydantic import EmailStr, validator, constr
from pydantic import BaseModel


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserPasswordBase(BaseModel):
    @validator("repeated_password", check_fields=False)
    def password_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Password do not match")
        return v

    password: constr(min_length=8)
    repeated_password: str


class UserCreate(UserBase, UserPasswordBase):
    """  """
    email: EmailStr
    username: str


class UserUpdate(UserBase, UserPasswordBase):
    password: Optional[constr(min_length=8)]
    repeated_password: Optional[str]
