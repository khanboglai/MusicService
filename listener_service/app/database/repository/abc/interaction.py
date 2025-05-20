from abc import ABC, abstractmethod
from typing import List

from domain.events.real.interaction import NewInteractionRegistered
from domain.entities.real.listener import Listener


class BaseInteractionRepo(ABC):
    @abstractmethod
    async def add_or_update_interaction(self, *, listener: Listener, track_id: int, listen_time: int) -> NewInteractionRegistered:
        ...

    @abstractmethod
    async def get_interaction_by_ids(self, *, listener: Listener, track_id: int) -> NewInteractionRegistered:
        ...
        
    @abstractmethod
    async def get_listener_history(self, *, listener: Listener) -> List[NewInteractionRegistered]:
        ...
