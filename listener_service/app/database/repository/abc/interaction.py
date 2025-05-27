""" Определение абстрактного слоя репозиториев для взаимодействий """
from abc import ABC, abstractmethod
from typing import List

from domain.events.real.interaction import NewInteractionRegistered, NewInteractionAnalyticsRegistered
from domain.entities.real.listener import Listener


class BaseInteractionRepo(ABC):
    """ Абстрактный слой репозиториев взаимодействий """
    @abstractmethod
    async def add_or_update_interaction(self, *, listener: Listener, track_id: int, listen_time: int, track_name: str, artist_id: int, artist_name: str, genre_id: int, genre_name: str) -> NewInteractionRegistered:
        ...

    # @abstractmethod
    # async def get_interaction_by_ids(self, *, listener: Listener, track_id: int) -> NewInteractionRegistered:
    #     ...

    # @abstractmethod
    # async def get_analytics_interaction_by_ids(self, *, listener: Listener, track_id: int) -> NewInteractionAnalyticsRegistered:
    #     ...
        
    @abstractmethod
    async def get_listener_history(self, *, listener: Listener) -> List[NewInteractionRegistered]:
        ...
