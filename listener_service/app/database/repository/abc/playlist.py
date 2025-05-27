""" Определение абстрактного слоя репозиториев для плейлистов """
from abc import ABC, abstractmethod

from domain.events.real.playlist import NewPlaylistRegistered, PlaylistTrack
from domain.entities.real.listener import Listener


class BasePlaylistRepo(ABC):
    """ Абстрактный слой репозиториев плейлистов """
    @abstractmethod
    async def get_playlist(self, *, playlist_id: int, listener: Listener) -> NewPlaylistRegistered: # Передаем также слушателя, чтобы он не получил доступ к чужим плейлистам
        ...

    @abstractmethod
    async def get_playlist_by_title(self, *, title: str, listener: Listener) -> NewPlaylistRegistered:
        ...

    @abstractmethod
    async def insert_playlist(self, *, listener: Listener, title: str) -> NewPlaylistRegistered:
        ...

    @abstractmethod
    async def delete_playlist(self, *, listener: Listener, playlist_id: int): # Передаем также слушателя, чтобы он не получил доступ к чужим плейлистам
        ...

    @abstractmethod
    async def get_all_playlists(self, *, listener: Listener) -> list[NewPlaylistRegistered]:
        ...
    
    @abstractmethod
    async def add_new_track_in_playlist(self, *, listener: Listener, playlist_id: int, track_id: int) -> PlaylistTrack:
        ...

    @abstractmethod
    async def get_track_in_playlist(self, *, playlist: NewPlaylistRegistered, track_id: int) -> PlaylistTrack:
        ...

    @abstractmethod
    async def delete_track_from_playlist(self, *, listener: Listener, playlist: NewPlaylistRegistered, track_id: int, from_user: bool = True):
        ...

    @abstractmethod
    async def get_tracks_in_playlist(self, *, listener: Listener, playlist_id: int) -> list[PlaylistTrack]:
        ...
