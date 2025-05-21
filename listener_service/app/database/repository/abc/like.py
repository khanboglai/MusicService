""" Определение абстрактного слоя репозиториев для лайка """
from abc import ABC, abstractmethod

from domain.events.real.like import NewLikeRegistered
from domain.entities.real.listener import Listener

class BaseLikeRepo(ABC):
    """ Абстрактный слой репозиториев для лайка """
    @abstractmethod
    async def get_like_by_ids(self, *, listener: Listener, track_id: int) -> NewLikeRegistered:
        ...

    @abstractmethod
    async def add_or_delete_like(self, *, listener: Listener, track_id: int) -> NewLikeRegistered:
        ...
        