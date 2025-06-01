from datetime import datetime
import grpc
import asyncio
from grpc import StatusCode
from concurrent import futures
from google.protobuf.timestamp_pb2 import Timestamp
from src.dependencies.repository import ArtistRepositoryFactory
from src.repositories.domain_repo import ArtistRepositoryABC
from src.database.postgres import get_db_session # только так получилось достать сессию для gRPC
from src.models.artist import Artist
from src.grpc.artist_pb2_grpc import add_ArtistServiceServicer_to_server
from src.grpc.artist_pb2 import (
    GetArtistDataByUserIdResponse,
    CreateArtistResponse,
    GetArtistDataByIdResponse,
    GetArtistIdResponse,
    DeleteArtistByUserIdResponse
)
from src.value_objects.artist_description import Description
from src.grpc.grpc_exceptions_handlers.grpc_excaption_handler import grpc_exception_handler
from src.core.logging import logger
from src.search import add_artist_to_es, rmv_artist_from_es


class ArtistService:
    def __init__(self, artist_repo: ArtistRepositoryABC):
        self.artist_repo = artist_repo

    @grpc_exception_handler # в декоратор поместил логику обработки ошибок, кода стало в 2 раза меньше
    async def CreateArtist(self, request, context):
        """ Функция для создания исполнителя """
        new_artist = Artist(
            name=request.name,
            email=request.email,
            registered_at=datetime.now(),
            description=Description(request.description),
            user_id=request.user_id
        )

        artist = await self.artist_repo.create_artist(new_artist)
        r = await add_artist_to_es(artist_id=artist.oid, title=artist.name)
        logger.info(f"GRPC: Created new artist {artist.name}")
        return CreateArtistResponse(artist_id=artist.oid) ## тут artist_id

    @grpc_exception_handler
    async def GetArtistDataByUserId(self, request, context):
        """ Функция для получения данных исполнителя по user_id """
        user_id = int(request.user_id)
        artist = await self.artist_repo.get_artist_by_user_id(user_id)
        logger.info(f"GRPC: Getting description for artist {artist.name}")
        timestamp = Timestamp()
        timestamp.FromDatetime(artist.registered_at)
        return GetArtistDataByUserIdResponse(
            id=artist.oid,
            name=artist.name,
            description=str(artist.description),
            registered_at=timestamp
        )

    @grpc_exception_handler
    async def GetArtistDataById(self, request, context):
        """ Функция для получения данных исполнителя по id из сервиса исполнителя """
        artist  = await self.artist_repo.get_artist_by_id(request.artist_id)
        logger.info(f"GRPC: Getting description [by artist id] for artist {artist.name}")
        timestamp = Timestamp()
        timestamp.FromDatetime(artist.registered_at)
        return GetArtistDataByIdResponse(
            id=artist.oid,
            name=artist.name,
            description=str(artist.description),
            registered_at=timestamp
        )


    @grpc_exception_handler
    async def GetArtistId(self, request, context):
        """ Функция для получения id исполнителя из сервиса """
        artist = await self.artist_repo.get_artist_by_user_id(request.user_id)
        logger.info(f"GRPC: Getting artist id for artist {artist.name}")
        return GetArtistIdResponse(id=artist.oid)


    @grpc_exception_handler
    async def DeleteArtistByUserId(self, request, context):
        """ Функция для удаления исполнителя по user_id """
        artist = await self.artist_repo.get_artist_by_user_id(request.user_id)
        user_id = await self.artist_repo.delete_artist(request.user_id)
        r = await rmv_artist_from_es(artist_id=artist.oid)
        logger.info(f"GRPC: Delete artist by user_id {user_id}")
        return DeleteArtistByUserIdResponse(user_id=user_id)

    # @grpc_exception_handler
    # async def UploadArtistCover(self, request_iterator, context):
    #
    #     buffer = io.BytesIO()
    #     user_id = None
    #
    #     try:
    #         s3_client = settings.create_minio_client()
    #         bucket_name = settings.minio_bucket_name
    #         settings.create_bucket_if_not_exists(client=s3_client)
    #
    #         async for chunk in request_iterator:
    #             if user_id is None:
    #                 user_id = chunk.user_id
    #             buffer.write(chunk.content)
    #
    #         if user_id is None:
    #             return UploadStatus(success=False, message="User id is missing")
    #
    #         artist = await self.artist_repo.get_artist_by_user_id(user_id)
    #         s3_key = f"{artist.oid}/{artist.oid}.jpg"
    #         buffer.seek(0) # перемещение указателя на начало буфера
    #
    #         # проверка типа файла
    #         mimetype = magic.from_buffer(buffer.read(1024), mime=True)
    #         buffer.seek(0)
    #         if mimetype != "image/jpeg":
    #             return UploadStatus(success=False, message="Unsupported Media Type")
    #         logger.info("GRPC: Checked mime type")
    #
    #         s3_client.upload_fileobj(
    #             Fileobj=buffer,
    #             Bucket=bucket_name,
    #             Key=s3_key,
    #             ExtraArgs={"ContentType": "image/jpeg"}
    #         )
    #
    #         logger.info("GRPC: Uploaded cover")
    #         return UploadStatus(success=True, message="Artist Cover Uploaded")
    #     finally:
    #         buffer.close()



async def serve(redis_client):
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    async with get_db_session() as db:
        repo = await ArtistRepositoryFactory.create(
            db=db,
            use_cache=True,
            redis_client=redis_client
        )

    service = ArtistService(repo)

    add_ArtistServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
