""" Определение события для лайка """
from uuid import UUID, uuid4

from domain.events.abc.base import BaseEvent


class NewLikeRegistered(BaseEvent):
    """ Событие лайка """
    user: UUID
    track_id: UUID
