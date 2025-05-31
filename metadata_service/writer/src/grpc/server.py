import grpc
from concurrent import futures
import asyncio

from src.common.dependencies.repository.album import AlbumRepositoryFactory
from src.common.dependencies.repository.track import TrackRepositoryFactory
from src.common.repository.abstract.album import AlbumRepositoryABC
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.database.session import get_db_session
from src.common.models.album import Album
from src.common.schemas.track import TrackCreate
from src.search import add_track_to_es, add_album_to_es, rmv_track_from_es, rmv_album_from_es
from src.config import settings

from src.grpc.writer_pb2_grpc import add_WriterServiceServicer_to_server
from src.grpc.writer_pb2 import (
    CreateAlbum_Response,
    RemoveAlbum_Response,
    RemoveAlbumsByOwnerID_Response,
    CreateTrack_Response,
    RemoveTrack_Response

)
from src.grpc.exceptions.handler import grpc_exception_handler
from src.common.core.logging import logger


class WriterService:
    """ gRPC сервис писателя """

    def __init__(self, artist_repo: AlbumRepositoryABC, track_repo: TrackRepositoryABC):
       self.album_repo = artist_repo
       self.track_repo = track_repo

    @grpc_exception_handler
    async def CreateAlbum(self, request, context):
        """ Процедура создания альбома """
        new_album = Album(
            title=request.title,
            owner_id=request.owner_id,
            release_date=request.release_date.ToDatetime().date(),
        )
        album = await self.album_repo.create_album(new_album)
        r = await add_album_to_es(album_id=album.oid, title=new_album.title)

        logger.info(f"gRPC -> CreateAlbum -> {album.oid}")
        return CreateAlbum_Response(album_id=album.oid)

    @grpc_exception_handler
    async def RemoveAlbum(self, request, context):
        """ Процедура удаления альбома """
        album_id = request.album_id
        
        tids = [track.track_id for track in self.track_repo.get_tracks_by_album_id(album_id)]

        id = await self.album_repo.remove_album(album_id)

        for tid in tids:
            r = await rmv_track_from_es(tid)

        logger.info(f"gRPC -> RemoveAlbum -> {id}")
        return RemoveAlbum_Response(album_id=id)

    @grpc_exception_handler
    async def RemoveAlbumsByOwnerID(self, request, context):
        """ Процедура удаления альбомов по ID владельца """
        owner_id = request.owner_id

        ids = await self.album_repo.remove_albums_by_owner_id(owner_id)
        for id in ids:
            tids = [track.track_id for track in self.track_repo.get_tracks_by_album_id(id)]
            r = await rmv_album_from_es(album_id=id)
            for tid in tids:
                r = await rmv_track_from_es(tid)
        logger.info(f"gRPC -> RemoveAlbumsByOwnerID -> {ids}")
        return RemoveAlbumsByOwnerID_Response(album_ids=ids)

    @grpc_exception_handler
    async def CreateTrack(self, request, context):
        """ Процедура создания трека """  
        new_track = TrackCreate(
            title=request.title,
            album_id=request.album_id,
            explicit=request.explicit,
            genre_names=request.genre_names
        )
        track = await self.track_repo.create_track(new_track)
        r = await add_track_to_es(track_id=track.oid, title=new_track.title)

        logger.info(f"gRPC -> CreateTrack -> {track.oid}")
        return CreateTrack_Response(track_id=track.oid)

    @grpc_exception_handler
    async def RemoveTrack(self, request, context):
        """ Процедура удаления трека """
        track_id = request.track_id

        id = await self.track_repo.remove_track(track_id)
        r = await rmv_track_from_es(track_id=id)

        logger.info(f"gRPC -> RemoveTrack -> {id}")
        return RemoveTrack_Response(track_id=id)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    async with get_db_session() as db:
        album_repo = await AlbumRepositoryFactory.create(db)
        track_repo = await TrackRepositoryFactory.create(db)

    servicer = WriterService(album_repo, track_repo)

    add_WriterServiceServicer_to_server(servicer, server)
    server.add_insecure_port("[::]:50051")

    logger.info("Writer gRPC server successfully started and runs on port 50051")

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
