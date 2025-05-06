from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import grpc
import asyncio
from concurrent import futures

from src.database.postgres import get_session
from src.models.artist import Artist
from src.repositories.artist_repo import ArtistRepository
from src.grpc.artist_pb2_grpc import add_ArtistServiceServicer_to_server
from src.grpc.artist_pb2 import GetDescriptionResponse, CreateArtistResponse
from src.value_objects.artist_description import Description


@asynccontextmanager
async def get_db_session():
    async for session in get_session():
        yield session

class ArtistService:
    async def CreateArtist(self, request, context):
        async with get_db_session() as db:
            repository = ArtistRepository(db)

            new_artist = Artist(
                name=request.name,
                email="<test1@mail.ru>",
                registered_at=datetime.now(),
                cover_path="test grpc",
                description=Description(request.description),
                user_id=101
            )
            artist = await repository.create_artist(new_artist)
            return CreateArtistResponse(id=artist.user_id)

    async def GetDescription(self, request, context):
        async with get_db_session() as db:
            repository = ArtistRepository(db)
            user_id = request.id
            artist = await repository.get_artist_by_user_id(user_id)
            return GetDescriptionResponse(description=artist.description)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ArtistServiceServicer_to_server(ArtistService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())