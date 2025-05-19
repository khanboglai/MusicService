import mimetypes
from datetime import datetime
import os
import io
import magic
import grpc
import asyncio

from grpc import StatusCode
from concurrent import futures
from src.database.postgres import get_db_session # только так получилось достать сессию для gRPC
from src.models.artist import Artist
from src.core.config import settings
from src.repositories.artist_repo import ArtistRepository
from src.grpc.artist_pb2_grpc import add_ArtistServiceServicer_to_server
from src.grpc.artist_pb2 import GetDescriptionResponse, CreateArtistResponse, FileChunk, UploadStatus
from src.value_objects.artist_description import Description
from src.grpc.grpc_exceptions_handlers.grpc_excaption_handler import grpc_exception_handler
from src.core.logging import logger





class ArtistService:
    @grpc_exception_handler # в декоратор поместил логику обработки ошибок, кода стало в 2 раза меньше
    async def CreateArtist(self, request, context):
        async with get_db_session() as db:
            repository = ArtistRepository(db)

            new_artist = Artist(
                name=request.name,
                email=request.email,
                registered_at=datetime.now(),
                description=Description(request.description),
                user_id=request.user_id
            )
            artist = await repository.create_artist(new_artist)
            return CreateArtistResponse(id=artist.user_id)


    @grpc_exception_handler
    async def GetDescription(self, request, context):
        async with get_db_session() as db:
            repository = ArtistRepository(db)
            user_id = int(request.user_id)
            artist = await repository.get_artist_by_user_id(user_id)
            return GetDescriptionResponse(description=str(artist.description))


    # @grpc_exception_handler
    async def UploadArtistCover(self, request_iterator, context):

        buffer = io.BytesIO()
        user_id = None

        try:
            s3_client = settings.create_minio_client()
            bucket_name = settings.minio_bucket_name
            settings.create_bucket_if_not_exists(client=s3_client)

            async for chunk in request_iterator:
                if user_id is None:
                    user_id = chunk.user_id
                buffer.write(chunk.content)

            if user_id is None:
                return UploadStatus(success=False, message="User id is missing")

            artist = None
            async with get_db_session() as db:
                repository = ArtistRepository(db)
                artist = await repository.get_artist_by_user_id(user_id)

            if artist is None:
                return UploadStatus(success=False, message=f"Artist with user_id {user_id} not found")


            s3_key = f"{artist.oid}/{artist.oid}.jpg"
            buffer.seek(0) # перемещение указателя на начало буфера

            # проверка типа файла
            mimetype = magic.from_buffer(buffer.read(1024), mime=True)
            buffer.seek(0)
            if mimetype != "image/jpeg":
                return UploadStatus(success=False, message="Unsupported Media Type")
            logger.info("Checked mime type")

            s3_client.upload_fileobj(
                Fileobj=buffer,
                Bucket=bucket_name,
                Key=s3_key,
                ExtraArgs={"ContentType": "image/jpeg"}
            )

            logger.info("Uploaded file")
            return UploadStatus(success=True, message="Artist Cover Uploaded")
        except Exception as e:
            return UploadStatus(success=False, message=str(e))
        finally:
            buffer.close()


    async def UploadFileMP3(self, request_iterator, context):
        pass


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ArtistServiceServicer_to_server(ArtistService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
