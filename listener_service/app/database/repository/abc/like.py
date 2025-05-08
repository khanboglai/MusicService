from abc import ABC, abstractmethod

from domain.events.real.like import NewLikeRegistered

class BaseLikeRepo(ABC):
    @abstractmethod
    async def add_like(self, *, like: NewLikeRegistered) -> NewLikeRegistered:
        ...

    @abstractmethod
    async def delete_like(self, *, user_id: int, track_id: int):
        ...
        