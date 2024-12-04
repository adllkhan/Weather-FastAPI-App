from datetime import datetime

from ..models import History as Model
from ..schemas import History as Schema, Histories as HistoriesSchema
from ..repositories import (
    HistoryRepositories as Repositories,
    UsersRepositories
)
from ..core import (
    NotFoundException,
    CannotCreateException,
    CannotDeleteException,
)


class Services:
    def __init__(self):
        self.repositories = Repositories()
        self.users = UsersRepositories()

    async def get(self, user_id: int) -> HistoriesSchema:
        history = await self.repositories.get(user_id=user_id)
        if not history:
            raise NotFoundException()
        res = HistoriesSchema(
            histories=[Schema.model_validate(h) for h in history]
        )
        return res

    async def create(
        self, history: Schema, user_id: int
    ) -> Schema:
        user = await self.users.get(_id=user_id)
        history_db = Model(
            city=history.city,
            temperature=history.temperature,
            description=history.description,
            longitude=history.longitude,
            latitude=history.latitude,
            created_at=datetime.now(),
            created_by_id=user_id,
            created_by=user
        )
        history_db = await self.repositories.create(history_db)
        if not history_db:
            raise CannotCreateException()
        return history

    async def delete(self, _id: int) -> Schema:
        history = await self.repositories.delete(_id=_id)
        if not history:
            raise CannotDeleteException()
        return Schema.model_validate(history)
