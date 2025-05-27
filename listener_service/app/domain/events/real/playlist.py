""" Определение события плейлиста (типа добавлен новый плейлист) """
from domain.events.abc.base import BaseEvent


class NewPlaylistRegistered(BaseEvent):
    """ Событие плейлиста """
    user: int
    title: str

    def __init__(self, user_id: int, title: str):
        self.user = user_id
        self.title = title


class PlaylistTrack:
    """ Связь между плейлистом и треком """
    playlist: int
    track_id: int

    def __init__(self, playlist_id: int, track_id: int):
        self.playlist = playlist_id
        self.track_id = track_id        
