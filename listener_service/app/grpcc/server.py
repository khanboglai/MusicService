from datetime import datetime
import grpc
import asyncio
from concurrent import futures
from domain.entities.real.listener import Listener
from database.repository.real.listener import ListenerRepository
# from src.repositories.domain_repo import ArtistRepositoryABC
from database.connect import get_db_session
# from src.database.postgres import get_db_session # только так получилось достать сессию для gRPC
# from src.models.artist import Artist
# from src.core.config import settings
from grpcc.listener_pb2_grpc import add_ListenerServiceServicer_to_server
from grpcc.listener_pb2 import GetListenerResponse
from domain.values.real.age import Age
from domain.values.real.name import Name
# from src.value_objects.artist_description import Description
# from src.grpc.grpc_exceptions_handlers.grpc_excaption_handler import grpc_exception_handler
from core.config import logger


class ListenerService:
    def __init__(self, listener_repo):
        self.listener_repo = listener_repo

    # @grpc_exception_handler # в декоратор поместил логику обработки ошибок, кода стало в 2 раза меньше
    # async def CreateArtist(self, request, context):

    #     new_artist = Artist(
    #         name=request.name,
    #         email=request.email,
    #         registered_at=datetime.now(),
    #         description=Description(request.description),
    #         user_id=request.user_id
    #     )
    #     artist = await self.artist_repo.create_artist(new_artist)
    #     logger.info(f"GRPC: Created new artist {artist.name}")
    #     return CreateArtistResponse(id=artist.user_id)


    # @grpc_exception_handler
    async def GetListener(self, request, context):
        listener_id = int(request.listener_id)
        listener = await self.listener_repo.get_listener(listener_id=listener_id)
        logger.info(f"GRPC: Getting description for artist {listener.first_name}")
        return GetListenerResponse(listener_id=listener.oid, user_id=listener.user_id, first_name=listener.first_name, last_name=listener.last_name)



    # @grpc_exception_handler
    # async def UploadArtistCover(self, request_iterator, context):

    #     buffer = io.BytesIO()
    #     user_id = None

    #     try:
    #         s3_client = settings.create_minio_client()
    #         bucket_name = settings.minio_bucket_name
    #         settings.create_bucket_if_not_exists(client=s3_client)

    #         async for chunk in request_iterator:
    #             if user_id is None:
    #                 user_id = chunk.user_id
    #             buffer.write(chunk.content)

    #         if user_id is None:
    #             return UploadStatus(success=False, message="User id is missing")

    #         artist = await self.artist_repo.get_artist_by_user_id(user_id)
    #         s3_key = f"{artist.oid}/{artist.oid}.jpg"
    #         buffer.seek(0) # перемещение указателя на начало буфера

    #         # проверка типа файла
    #         mimetype = magic.from_buffer(buffer.read(1024), mime=True)
    #         buffer.seek(0)
    #         if mimetype != "image/jpeg":
    #             return UploadStatus(success=False, message="Unsupported Media Type")
    #         logger.info("GRPC: Checked mime type")

    #         s3_client.upload_fileobj(
    #             Fileobj=buffer,
    #             Bucket=bucket_name,
    #             Key=s3_key,
    #             ExtraArgs={"ContentType": "image/jpeg"}
    #         )

    #         logger.info("GRPC: Uploaded cover")
    #         return UploadStatus(success=True, message="Artist Cover Uploaded")
    #     finally:
    #         buffer.close()


    # async def UploadFileMP3(self, request_iterator, context):
    #     pass


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    async with get_db_session() as db:
        # repo = await ArtistRepositoryFactory.create(
        #     db=db,
        #     use_cache=True,
        #     redis_client=redis_client
        # )
        repo = ListenerRepository(db)

    service = ListenerService(repo)

    add_ListenerServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())