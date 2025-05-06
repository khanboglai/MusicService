import grpc
from app.grpc_clients.artist_pb2_grpc import ArtistServiceStub
from app.grpc_clients.artist_pb2 import GetDescriptionRequest, CreateArtistRequest

class ArtistClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('artist_web:50051')
        self.stub = ArtistServiceStub(self.channel)

    def create_artist(self, name, description):
        # Создаем запрос
        request = CreateArtistRequest(name=name, description=description)
        # Вызываем метод сервера
        response = self.stub.CreateArtist(request)
        return response.id