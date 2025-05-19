""" Определения события взаимодействия """
from datetime import datetime

from domain.events.abc.base import BaseEvent


class NewInteractionRegistered(BaseEvent):
    """ Событие взаимодействия """
    user: int
    track_id: int
    last_interaction: datetime
    count_interaction: int
    listen_time: int # в секундах
    
    def __init__(self, listener_id: int, track_id: int, listen_time: int):
        self.user = listener_id
        self.track_id = track_id
        self.last_interaction = datetime.now()
        self.count_interaction = 1
        self.listen_time = listen_time
    