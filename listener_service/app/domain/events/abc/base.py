""" Определение абстрактного события """
from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class BaseEvent(ABC):
    """ Абстрактное событие """
    event_id: UUID = field(
        default_factory=uuid4
    )
