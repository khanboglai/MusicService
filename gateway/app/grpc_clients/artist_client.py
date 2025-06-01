""" Клиент gRPC для взаимодействия с сервером исполнителя """

import grpc
from app.grpc_clients.artist_pb2_grpc import ArtistServiceStub
from app.grpc_clients.artist_pb2 import (
    GetArtistDataByUserIdRequest,
    CreateArtistRequest,
    GetArtistDataByIdRequest,
    GetArtistIdRequest,
    DeleteArtistByUserIdRequest
)
from app.schemas.artist import ArtistCreate
from app.grpc_clients.grpc_client_exception_handler import grpc_client_exception_handler


class ArtistClient:
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('artist_web:50051')
        self.stub = ArtistServiceStub(self.channel)

    @grpc_client_exception_handler
    async def create_artist(self, artist: ArtistCreate, user_id: int):
        """ Функция для передачи запроса для создания исполнителя """
        # создаем запрос
        request = CreateArtistRequest(
            name=artist.name,
            email=artist.email,
            description=artist.description,
            user_id=user_id,
        )
        # вызываем метод сервера
        response = await self.stub.CreateArtist(request)
        return response.artist_id


    @grpc_client_exception_handler
    async def get_data_by_user_id(self, user_id: int):
        """ Функция для передачи запроса с user_id исполнителя и возврата описания исполнителя """
        request = GetArtistDataByUserIdRequest(user_id=user_id)
        response = await self.stub.GetArtistDataByUserId(request)
        return response.id, response.name, response.description, response.registered_at.ToDatetime().strftime("%Y-%m-%d %H:%M:%S")


    @grpc_client_exception_handler
    async def get_data_by_artist_id(self, artist_id: int):
        """ Функция для передачи запроса с id исполнителя и возврата его описания """
        request = GetArtistDataByIdRequest(artist_id=artist_id)
        response = await self.stub.GetArtistDataById(request)
        return response.id, response.name, response.description, response.registered_at.ToDatetime().strftime("%Y-%m-%d %H:%M:%S")


    @grpc_client_exception_handler
    async def delete_artist(self, user_id: int):
        """ Функция для передачи запроса на удаление исполнителя. Возврат: user_id в случае успеха """
        request = DeleteArtistByUserIdRequest(user_id=user_id)
        response = await self.stub.DeleteArtistByUserId(request)
        return response.user_id


    @grpc_client_exception_handler
    async def get_artist_id(self, user_id: int):
        """ Функция для получения локального id исполнителя """
        request = GetArtistIdRequest(user_id=user_id)
        response = await self.stub.GetArtistId(request)
        return response.id


    # @grpc_client_exception_handler
    # async def upload_cover(self, file_path: str, user_id: int):
    #     def generate_chunks():
    #         with open(file_path, 'rb') as f:
    #             while True:
    #                 chunk = f.read(1024 * 64) # читаем по частям 64 Кб
    #                 if not chunk:
    #                     break
    #                 yield FileChunk(content=chunk, user_id=user_id)
    #
    #     response = await self.stub.UploadArtistCover(generate_chunks())
    #     return response
