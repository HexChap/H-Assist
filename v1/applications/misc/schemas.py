from pydantic import BaseModel


class InfoResponse(BaseModel):
    api_version: str
    build_version: str
