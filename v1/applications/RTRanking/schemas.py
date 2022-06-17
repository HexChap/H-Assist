from typing import Optional

from pydantic import BaseModel

from v1.applications.user import schemas


class CompetitorBase(BaseModel):
    added_by: Optional[schemas.UserBase]
    name: str
    start_number: int
    is_highlighted: bool = False

    class Config:
        arbitrary_types_allowed = True
