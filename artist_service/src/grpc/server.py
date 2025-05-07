from datetime import datetime
import grpc
import asyncio
from grpc import StatusCode
from concurrent import futures
from src.database.postgres import get_db_session # только так получилось достать сессию для gRPC
from src.models.artist import Artist
from src.repositories.artist_repo import ArtistRepository
from src.grpc.artist_pb2_grpc import add_ArtistServiceServicer_to_server
from src.grpc.artist_pb2 import GetDescriptionResponse, CreateArtistResponse
from src.value_objects.artist_description import Description
from src.grpc.grpc_exceptions_handlers.grpc_excaption_handler import grpc_exception_handler


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


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ArtistServiceServicer_to_server(ArtistService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
