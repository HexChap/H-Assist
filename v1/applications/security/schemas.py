from pydantic import BaseModel


class CustomPasswordRequestForm(BaseModel):
    email: str
    password: str
