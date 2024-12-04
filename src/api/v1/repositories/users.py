from sqlalchemy import select

from ..database import session
from ..models import User


class Repositories:
    def __init__(self):
        self.session = session

    async def get(self, _id: int) -> User:
        async with self.session() as session:
            result = await session.execute(select(User).filter_by(id=_id))
            return result.scalars().first()

    async def get_by_username(self, username: str) -> User:
        async with self.session() as session:
            result = await session.execute(
                select(User).filter_by(username=username)
            )
            return result.scalars().first()

    async def create(self, user: User) -> User:
        async with self.session() as session:
            session.add(user)
            await session.commit()
            return user

    async def update(self, user: User) -> User:
        async with self.session() as session:
            result = await session.execute(select(User).filter_by(id=user.id))
            delete_user = result.scalars().first()
            if not delete_user:
                return
            new_user = User(**user.dict())
            session.delete(delete_user)
            session.add(new_user)
            await session.commit()
            return new_user

    async def delete(self, _id: int) -> User:
        async with self.session() as session:
            result = await session.execute(select(User).filter_by(id=_id))
            delete_user = result.scalars().first()
            if not delete_user:
                return
            session.delete(delete_user)
            await session.commit()
            return delete_user
