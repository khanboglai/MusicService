""" Определение события для лайка """
from domain.events.abc.base import BaseEvent


class NewLikeRegistered(BaseEvent):
    """ Событие лайка """
    user: int
    track_id: int
