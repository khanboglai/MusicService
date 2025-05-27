from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.repository.abc.playlist import BasePlaylistRepo
from domain.events.real.playlist import NewPlaylistRegistered, PlaylistTrack
from database.exceptions.real.unique import UniqueException
from database.exceptions.real.existance import NotExistException
from database.exceptions.real.forbidden import ForbiddenDeletingException, ForbiddenInsertingException
from database.exceptions.abc.base import DatabaseErrorException, DatabaseException
from domain.entities.real.listener import Listener


class PlaylistRepository(BasePlaylistRepo):
    """ Слой репозиториев для плейлистов """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_playlist(self, *, playlist_id: int, listener: Listener) -> NewPlaylistRegistered:
        """ Получение плейлиста """
        statement = (
            select(NewPlaylistRegistered)
            .where(
                (NewPlaylistRegistered.event_id == playlist_id) &
                (NewPlaylistRegistered.user == listener)
            )
        )
        result = await self.session.execute(statement=statement)
        result = result.scalar_one_or_none()
        if not result:
            raise NotExistException
        return result
    
    async def get_playlist_by_title(self, *, title: str, listener: Listener) -> NewPlaylistRegistered:
        """ Получение плейлиста по названию """
        statement = (
            select(NewPlaylistRegistered)
            .where(
                (NewPlaylistRegistered.title == title) &
                (NewPlaylistRegistered.user == listener)
            )
        )
        result = await self.session.execute(statement=statement)
        result = result.scalar_one_or_none()
        if not result:
            raise NotExistException
        return result
    
    async def insert_playlist(self, *, listener: Listener, title: str) -> NewPlaylistRegistered:
        """ Добавление плейлиста """
        try:
            exist_playlist = await self.get_playlist_by_title(title=title, listener=listener)
            raise UniqueException
        except NotExistException:
            playlist = NewPlaylistRegistered(user_id=listener, title=title)
            self.session.add(playlist)
            await self.session.commit()
            await self.session.refresh(playlist)
            return playlist
        
    async def delete_playlist(self, *, listener: Listener, playlist_id: int):
        """ Удаление плейлиста """
        try:
            playlist = await self.get_playlist(playlist_id=playlist_id, listener=listener)
            if playlist.title == "liked":
                raise ForbiddenDeletingException
            await self.session.delete(playlist)
            await self.session.commit()
        except NotExistException:
            raise NotExistException

    async def get_all_playlists(self, *, listener: Listener) -> list[NewPlaylistRegistered]:
        """ Получение всех плейлистов слушателя """
        statement = (
            select(NewPlaylistRegistered)
            .where(NewPlaylistRegistered.user == listener)
        )
        result = await self.session.execute(statement=statement)
        playlists = result.scalars().all()

        if playlists is None:
            playlists = []
        return playlists
    
    async def add_new_track_in_playlist(self, *, listener: Listener, playlist_id: int, track_id: int, from_user: bool = True) -> PlaylistTrack:
        """ Добавление нового трека в плейлист """
        try:
            playlist = await self.get_playlist(playlist_id=playlist_id, listener=listener)
            if playlist.title == "liked" and from_user:
                raise ForbiddenInsertingException
            statement = (
                select(PlaylistTrack)
                .where(
                    (PlaylistTrack.playlist == playlist) &
                    (PlaylistTrack.track_id == track_id)
                )
            )
            result = await self.session.execute(statement=statement)
            result = result.scalar_one_or_none()
            if result:
                raise UniqueException
            playlist_track = PlaylistTrack(playlist_id=playlist, track_id=track_id)
            self.session.add(playlist_track)
            await self.session.commit()
            await self.session.refresh(playlist_track)
            return playlist_track
        except NotExistException:
            raise NotExistException
        
    async def get_track_in_playlist(self, *, playlist: NewPlaylistRegistered, track_id: int) -> PlaylistTrack:
        """ Получение трека из плейлиста """
        statement = (
            select(PlaylistTrack)
            .where(
                (PlaylistTrack.playlist == playlist) &
                (PlaylistTrack.track_id == track_id)
            )
        )
        result = await self.session.execute(statement=statement)
        result = result.scalar_one_or_none()
        if not result:
            raise NotExistException
        return result
        
    async def delete_track_from_playlist(self, *, listener: Listener, playlist_id: int, track_id: int, from_user: bool = True): # from user - флаг того, что мы удаляем трек по запросу юзера, а не сервиса
        """ Удаление трека из плейлиста """
        try:
            playlist = await self.get_playlist(playlist_id=playlist_id, listener=listener)
            if playlist.title == "liked" and from_user:
                raise ForbiddenDeletingException
            playlist_track = await self.get_track_in_playlist(playlist=playlist, track_id=track_id)
            await self.session.delete(playlist_track)
            await self.session.commit()
        except NotExistException:
            raise NotExistException
        
    async def get_tracks_in_playlist(self, *, listener: Listener, playlist_id: int) -> list[PlaylistTrack]:
        """ Получение всех треков из плейлистов """
        try:
            playlist = await self.get_playlist(playlist_id=playlist_id, listener=listener)
            statement = (
                select(PlaylistTrack)
                .where(PlaylistTrack.playlist == playlist)
            )
            result = await self.session.execute(statement=statement)
            tracks = result.scalars().all()

            if tracks is None:
                tracks = []
            return tracks
        except NotExistException:
            raise NotExistException
