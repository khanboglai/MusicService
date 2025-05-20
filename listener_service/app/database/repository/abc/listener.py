from abc import ABC, abstractmethod
from domain.entities.real.listener import Listener


class BaseListenerRepo(ABC):
    @abstractmethod
    async def get_listener(self, *, listener_id: int) -> Listener:
        ...

    @abstractmethod
    async def get_listener_by_user_id(self, *, user_id: int) -> Listener:
        ...

    @abstractmethod
    async def insert_listener(self, *, listener: Listener) -> Listener:
        ...

    @abstractmethod
    async def delete_listener(self, *, user_id: int) -> None:
        ...
