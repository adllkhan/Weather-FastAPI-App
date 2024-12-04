from sqlalchemy import select

from ..database import session
from ..models import History


class Repositories:
    def __init__(self):
        self.session = session

    async def get(self, user_id: int) -> list[History]:
        async with self.session() as session:
            result = await session.execute(
                select(History).filter_by(created_by_id=user_id)
            )
            return result.scalars().all()

    async def create(self, history: History) -> History:
        async with self.session() as session:
            session.add(history)
            await session.commit()
            return history

    async def delete(self, _id: int, user_id: int) -> History:
        async with self.session() as session:
            result = await session.execute(
                select(History).filter_by(id=_id, created_by_id=user_id)
            )
            delete_history = result.scalars().first()
            if not delete_history:
                return
            await session.delete(delete_history)
            await session.commit()
            return delete_history
