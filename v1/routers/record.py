from fastapi import APIRouter, HTTPException, status, Depends

from v1.applications.record import schemas, RecordCRUD
from v1.core.dependencies import get_current_active_user

__tags__ = ["record"]
__prefix__ = "/record"

router = APIRouter()


@router.post("/", response_model=schemas.RecordResponse)
async def create(
        *,
        payload: schemas.RecordPayload,
        current_user=Depends(get_current_active_user)
):
    return await RecordCRUD.create(payload, current_user.id)


@router.get("/", response_model=list[schemas.RecordResponse])
async def get_all(_=Depends(get_current_active_user)):
    return await RecordCRUD.get_all()


@router.get("/{record_id}", response_model=schemas.RecordResponse)
async def get_by_id(
    record_id: int,
    current_user=Depends(get_current_active_user)
):
    l_data = await RecordCRUD.get(record_id)

    if current_user.id == (await l_data.user).id:
        return l_data

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot view other users' records"
        )
