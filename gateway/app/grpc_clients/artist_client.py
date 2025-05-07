""" Клиент gRPC для взаимодействия с сервером исполнителя """

import grpc
from app.grpc_clients.artist_pb2_grpc import ArtistServiceStub
from app.grpc_clients.artist_pb2 import GetDescriptionRequest, CreateArtistRequest
from app.schemas.artist import ArtistCreate
from app.grpc_clients.grpc_client_exception_handler import grpc_client_exception_handler

class ArtistClient:
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('artist_web:50051')
        self.stub = ArtistServiceStub(self.channel)

    @grpc_client_exception_handler
    async def create_artist(self, artist: ArtistCreate):
        # создаем запрос
        request = CreateArtistRequest(
            name=artist.name,
            email=artist.email,
            description=artist.description,
            user_id=artist.user_id,
        )
        # вызываем метод сервера
        response = await self.stub.CreateArtist(request)
        return response.id


    @grpc_client_exception_handler
    async def get_description(self, user_id: int):
        request = GetDescriptionRequest(user_id=user_id)
        response = await self.stub.GetDescription(request)
        return response.description
