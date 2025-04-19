""" Опреление абстрактной сущности """
from dataclasses import dataclass, field
from uuid import uuid4, UUID
from abc import ABC
from copy import copy

from domain.events.abc.base import BaseEvent


@dataclass
class BaseEntity(ABC):
    """ Абстрактная сущность """
    oid: UUID = field(
        default_factory=uuid4,
    )
    events: list[BaseEvent] = field(
        default_factory=list,
    )

    def register_event(self, event: BaseEvent):
        self.events.append(event)

    def pull_events(self, event: BaseEvent):
        registered_events = copy(self.events)
        self.events.clear()

        return registered_events
    