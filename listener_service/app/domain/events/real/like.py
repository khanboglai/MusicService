""" Определение события для лайка """
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from domain.events.abc.base import BaseEvent


@dataclass
class NewLikeRegistered(BaseEvent):
    """ Событие лайка """
    user_id: UUID = field(
        default_factory=uuid4
    )
    track_id: UUID = field(
        default_factory=uuid4
    )
