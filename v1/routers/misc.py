from fastapi import APIRouter, responses

from v1.core import settings
from v1.applications.misc import schemas

__tags__ = ["misc"]
__prefix__ = ""

router = APIRouter()


@router.get("/api-info", response_model=schemas.InfoResponse)
async def get_api_info():
    return schemas.InfoResponse(
        api_version=settings.api.version,
        build_version=settings.api.build_version
    )
