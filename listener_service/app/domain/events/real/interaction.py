""" Определения события взаимодействия """
from datetime import datetime

from domain.events.abc.base import BaseEvent


class NewInteractionRegistered(BaseEvent):
    """ Событие взаимодействия """
    user: int
    track_id: int
    last_interaction: datetime
    # count_interaction: int
    listen_time: int # в секундах
    
    def __init__(self, user_id: int, track_id: int, listen_time: int):
        self.user = user_id
        self.track_id = track_id
        self.last_interaction = datetime.now()
        # self.count_interaction = 1
        self.listen_time = listen_time


class NewInteractionAnalyticsRegistered(BaseEvent):
    """ Событие взаимодействия для аналитики """
    user: int
    track_id: int
    last_interaction: datetime
    # count_interaction: int
    listen_time: int
    track_name: str
    artist_id: int
    artist_name: str
    genre_id: int
    genre_name: str

    def __init__(self, user_id: int, track_id: int, listen_time: int, track_name: str, artist_id: int, artist_name: str, genre_id: int, genre_name: str):
        self.user = user_id
        self.track_id = track_id
        self.last_interaction = datetime.now()
        # self.count_interaction = 1
        self.listen_time = listen_time
        self.track_name = track_name
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.genre_id = genre_id
        self.genre_name = genre_name
    