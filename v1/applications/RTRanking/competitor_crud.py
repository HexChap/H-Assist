from typing import Union

from .models import Competitor
from .schemas import CompetitorBase
from v1.applications.user import User, UserCRUD


class CompetitorCRUD:
    def __init__(self):
        self.competitor_orm = Competitor

    async def get_all(self) -> list[Competitor]:
        return await self.competitor_orm.all()

    async def get_by_user(self, user: User) -> list[Competitor]:
        return await self.competitor_orm.filter(added_by=user.id).all()

    async def get_by_start_number(self, start_number: int) -> Competitor:
        return await self.competitor_orm.get(start_number=start_number)

    async def get_by_id(self, id: int) -> Competitor:
        return await self.competitor_orm.get(id=id)

    async def create(self, payload: CompetitorBase, added_by_id: int) -> Competitor:
        payload.added_by = await UserCRUD().get_by_id(added_by_id)
        payload.name = f"Competitor {payload.start_number}" if not payload.name else payload.name

        return await self.competitor_orm.create(**payload.dict())

    async def update_competitor(self, id: int, payload: Union[CompetitorBase, dict]):
        if isinstance(payload, CompetitorBase):
            payload = payload.dict()

        competitor = (await self.get_by_id(id)).update_from_dict(payload)
        await competitor.save()

        return competitor

    async def highlight(self, id: int):
        return await self.update_competitor(id, {"is_highlighted": True})

    async def disgrace(self, id: int):
        return await self.update_competitor(id, {"is_highlighted": False})
