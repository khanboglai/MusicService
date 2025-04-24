""" Опреление абстрактной сущности """
from uuid import uuid4, UUID
from abc import ABC
from copy import copy

from domain.events.abc.base import BaseEvent


class BaseEntity(ABC):
    """ Абстрактная сущность """
    oid: int
    events: list[BaseEvent]

    def register_event(self, event: BaseEvent):
        self.events.append(event)

    def pull_events(self):
        registered_events = copy(self.events)
        self.events.clear()

        return registered_events
    