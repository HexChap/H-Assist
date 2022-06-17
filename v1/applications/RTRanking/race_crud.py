from . import models
from .competitor_crud import CompetitorCRUD


class RaceCRUD:
    def __init__(self, race_orm: models.Race = models.Race):
        self.race_orm = race_orm
        self.competitors = CompetitorCRUD()

    async def get_all(self):
        return await self.race_orm.all()

    async def get_by_id(self, id: int):
        return await self.race_orm.get(id=id)

    async def get_all_competitors(self):
        return await self.competitors.get_all()

    async def create(self):
        pass

    async def update(self):
        pass

    async def add_competitor(self):
        pass
