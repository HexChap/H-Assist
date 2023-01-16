import datetime

from pydantic import BaseModel, constr


class RecordPayload(BaseModel):
    title: str
    note: constr(max_length=256)


class RecordResponse(BaseModel):
    id: int
    title: str
    note: str
    created_at: datetime.datetime
