""" Определения события взаимодействия """
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from domain.events.abc.base import BaseEvent


@dataclass
class NewInteractionRegistered(BaseEvent):
    """ Событие взаимодействия """
    user_id: UUID = field(
        default_factory=uuid4
    )
    track_id: UUID = field(
        default_factory=uuid4
    )
    last_interaction: datetime
    count_interaction: int
    listen_time: datetime.time # Надо потестить что это за тип
    