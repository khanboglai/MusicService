from uuid import UUID
from datetime import date

from infra.database.connect import async_session_maker
from domain.entities.real.listener import Listener
from domain.values.real.age import Age
from domain.values.real.name import Name


class ListenerRepository():
    def __init__(self):
        self.session = async_session_maker()

    async def add_listener(self, firstname: str, lastname: str, birthdate: str) -> Listener:
        new_listener = Listener.add_listener(Name(firstname), Name(lastname), Age(date.fromisoformat(birthdate))) # Тут возможно надо будет обрабатывать исключения + преобразователь дат
        self.session.add(new_listener)
        await self.session.commit()
        return new_listener
    
    async def get_listener_by_id(self, listener_id: UUID) -> Listener:
        listener = self.session.query(Listener).filter(Listener.oid == listener_id).first()
        return Listener
    
    async def close(self):
        await self.session.close()
