from fastapi import APIRouter, HTTPException, status

from v1.applications.RTRanking import CompetitorCRUD, RaceCRUD, models, schemas
from v1.applications.user import UserCRUD

__tags__ = ["rt_rating"]
__prefix__ = "/api/v1/races"

router = APIRouter()
competitors = CompetitorCRUD()
races = RaceCRUD()
users = UserCRUD()


@router.get("/")
async def get_all() -> list[models.Race]:
    return await races.get_all()


@router.get("/{race}/competitors")
async def get_all_competitors(race_id: int) -> list[models.Competitor]:
    race = RaceCRUD(races.get_by_id(race_id))
    return await race.get_all_competitors()


@router.get("/competitors/{number}")
async def get_by_start_number(number: int) -> models.Competitor:
    return await competitors.get_by_start_number(number)


@router.post("/")
async def create(
    *,
    payload: schemas.CompetitorBase,
    added_by_id: int,
) -> models.Competitor:
    # TODO: SPECIFIED RACE 50%
    return await competitors.create(payload, added_by_id)


@router.put("/highlight")
async def highlight(id: int):
    if (await competitors.get_by_id(id)).is_highlighted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The competitor is already highlighted"
        )
    return await competitors.highlight(id)


@router.put("/disgrace")
async def disgrace(id: int):
    if (await competitors.get_by_id(id)).is_highlighted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The competitor is not highlighted"
        )
    return await competitors.disgrace(id)
