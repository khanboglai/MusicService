""" Определение события для лайка """
from domain.events.abc.base import BaseEvent


class NewLikeRegistered(BaseEvent):
    """ Событие лайка """
    user: int
    track_id: int

    def __init__(self, listener_id: int, track_id: int):
        self.user = listener_id
        self.track_id = track_id
