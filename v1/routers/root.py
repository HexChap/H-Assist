from fastapi.responses import HTMLResponse
from fastapi import APIRouter

__tags__ = ["root"]
__prefix__ = ""

router = APIRouter()


@router.get("/")
async def root():
    return HTMLResponse("<h1>Welcome to H-Assist!</h1>")
