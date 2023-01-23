import uvicorn as uvicorn
from fastapi import FastAPI

from v1.core import settings
from v1.core.utilities import configure_db, include_routers

application = FastAPI(
    title=settings.api.title,
    version=f"{settings.api.version}.{settings.api.build_version}"
)


configure_db(application)
include_routers(application)


if __name__ == "__main__":
    uvicorn.run("main:application", reload=True)
