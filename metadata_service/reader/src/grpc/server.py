""" Cерверная часть сервиса ридера """
import grpc
import asyncio
from concurrent import futures

from src.common.dependencies.repository.album import AlbumRepositoryFactory
from src.common.dependencies.repository.track import TrackRepositoryFactory
from src.common.repository.abstract.album import AlbumRepositoryABC
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.database.session import get_db_session
from src.grpc.reader_pb2_grpc import add_ReaderServiceServicer_to_server
from src.grpc.reader_pb2 import (
    GetTrackResponse,
    GetTracksInAlbumResponse,
    GetAlbumResponse,
    GetAlbumInArtistResponse,
    GetTrackGenreResponse,
)
from src.common.core.logging import logger
from src.grpc.exceptions.handler import grpc_exception_handler


class ReaderService:
    """ Сервис ридера """
    def __init__(self, track_repo, album_repo):
        self.track_repo = track_repo
        self.album_repo = album_repo

    
    @grpc_exception_handler
    async def GetTrack(self, request, context):
        """ Ручка для получения информации о треке """
        track_id = int(request.track_id)
        track = await self.track_repo.get_track_by_id(id=track_id)
        logger.info(f"GRPC: Getting track data for track with track_id {track_id}")
        return GetTrackResponse(track_id=track.oid, title=track.title, album_id=track.album_id, explicit=track.explicit)
    
    @grpc_exception_handler
    async def GetTracksInAlbum(self, request, context):
        """ Ручка для получения треков в альбоме """
        album_id = int(request.album_id)
        tracks = await self.track_repo.get_tracks_by_album_id(album_id=album_id)
        logger.info(f"GRPC: Getting tracks in album with album_id {album_id}")
        return GetTracksInAlbumResponse(tracks=[GetTrackResponse(track_id=track.oid, title=track.title, album_id=track.album_id, explicit=track.explicit) for track in tracks])
    
    @grpc_exception_handler
    async def GetAlbum(self, request, context):
        """ Ручка для получения информации об альбоме """
        album_id = int(request.album_id)
        album = await self.album_repo.get_album_by_id(id=album_id)
        logger.info(f"GRPC: Getting album data for album with album_id {album_id}")
        return GetAlbumResponse(album_id=album.oid, title=album.title, artist_id=album.owner_id, release_date=str(album.release_date))
    
    @grpc_exception_handler
    async def GetAlbumInArtist(self, request, context):
        """ Ручка для получения альбомов исполнителя """
        artist_id = int(request.artist_id)
        albums = await self.album_repo.get_albums_by_owner_id(owner_id=artist_id)
        logger.info(f"GRPC: Getting albums in artist with artist_id {artist_id}")
        return GetAlbumInArtistResponse(albums=[GetAlbumResponse(album_id=album.oid, title=album.title, artist_id=album.owner_id, release_date=str(album.release_date)) for album in albums])
    
    @grpc_exception_handler
    async def GetTrackGenre(self, request, context):
        """ Ручка для получения жанра трека """
        track_id = int(request.track_id)
        genre = await self.track_repo.get_track_genre(track_id=track_id)
        logger.info(f"GRPC: Getting genre of track with track_id {track_id}")
        return GetTrackGenreResponse(genre_id=genre[0], genre_name=genre[1])
    

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    async with get_db_session() as db:
        # repo = await ArtistRepositoryFactory.create(
        #     db=db,
        #     use_cache=True,
        #     redis_client=redis_client
        # )
        album_repo = await AlbumRepositoryFactory.create(db)
        track_repo = await TrackRepositoryFactory.create(db)

    service = ReaderService(
        track_repo=track_repo,
        album_repo=album_repo,
    )

    add_ReaderServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
