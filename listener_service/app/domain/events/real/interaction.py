""" Определения события взаимодействия """
from datetime import datetime
from uuid import UUID, uuid4

from domain.events.abc.base import BaseEvent


class NewInteractionRegistered(BaseEvent):
    """ Событие взаимодействия """
    user: int
    track_id: int
    last_interaction: datetime
    count_interaction: int
    listen_time: datetime.time # Надо потестить что это за тип
    