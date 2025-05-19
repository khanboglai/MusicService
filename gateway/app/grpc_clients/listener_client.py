""" Клиент gRPC для взаимодействия с сервером исполнителя """

import grpc
from app.grpc_clients.listener_pb2_grpc import ListenerServiceStub
from app.grpc_clients.listener_pb2 import GetListenerRequest
# from app.schemas.artist import ArtistCreate
from app.grpc_clients.grpc_client_exception_handler import grpc_client_exception_handler

class ListenerClient:
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('web:50051') # change
        self.stub = ListenerServiceStub(self.channel)

    # @grpc_client_exception_handler
    # async def create_artist(self, artist: ArtistCreate):
    #     # создаем запрос
    #     request = CreateArtistRequest(
    #         name=artist.name,
    #         email=artist.email,
    #         description=artist.description,
    #         user_id=artist.user_id,
    #     )
    #     # вызываем метод сервера
    #     response = await self.stub.CreateArtist(request)
    #     return response.id


    @grpc_client_exception_handler
    async def get_listener(self, listener_id: int):
        request = GetListenerRequest(listener_id=listener_id)
        response = await self.stub.GetListener(request)
        return response


    # @grpc_client_exception_handler
    # async def upload_cover(self, file_path: str, user_id: int):
    #     def generate_chunks():
    #         with open(file_path, 'rb') as f:
    #             while True:
    #                 chunk = f.read(1024 * 64) # читаем по частям 64 Кб
    #                 if not chunk:
    #                     break
    #                 yield FileChunk(content=chunk, user_id=user_id)

    #     response = await self.stub.UploadArtistCover(generate_chunks())
    #     return response
