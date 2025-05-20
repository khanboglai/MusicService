from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from database.repository.abc.listener import BaseListenerRepo
from domain.entities.real.listener import Listener


class ListenerRepository(BaseListenerRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_listener(self, *, listener_id: int) -> Listener:
        statement = (
            select(Listener)
            .where(Listener.oid == listener_id)
        )
        result = await self.session.execute(statement=statement)
        return result.scalar_one_or_none()
    
    async def get_listener_by_user_id(self, *, user_id: int) -> Listener:
        statement = (
            select(Listener)
            .where(Listener.user_id == user_id)
        )
        result = await self.session.execute(statement=statement)
        return result.scalar_one_or_none()
    
    async def insert_listener(self, *, listener: Listener) -> Listener:
        self.session.add(listener)
        await self.session.commit()
        return listener
    
    async def delete_listener(self, *, user_id: int):
        listener = await self.get_listener_by_user_id(user_id=user_id)
        await self.session.delete(listener)
        await self.session.commit()

