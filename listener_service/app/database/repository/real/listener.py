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
    
    async def insert_listener(self, *, listener: Listener) -> Listener: # исключения и транзакции
        self.session.add(listener)
        await self.session.commit()
        return listener

    # async def add_listener(self, firstname: str, lastname: str, birthdate: str) -> Listener:
    #     new_listener = Listener.add_listener(Name(firstname), Name(lastname), Age(date.fromisoformat(birthdate))) # Тут возможно надо будет обрабатывать исключения + преобразователь дат
    #     self.session.add(new_listener)
    #     await self.session.commit()
    #     return new_listener
    
    # async def close(self):
    #     await self.session.close()
