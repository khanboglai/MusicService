""" Клиент gRPC для взаимодействия с сервером слушателя """
import grpc
from app.grpc_clients.listener_pb2_grpc import ListenerServiceStub
from app.grpc_clients.listener_pb2 import (
    GetListenerRequest,
    CreateListenerRequest,
    DeleteListenerRequest,
    LikeRequest,
    InteractionRequest,
    HistoryRequest,
    CreatePlaylistRequest,
    DeletePlaylistRequest,
    GetAllPlaylistsRequest,
    AddNewTrackInPlaylistRequest,
    DeleteTrackFromPlaylistRequest,
    GetAllTracksInPlaylistRequest,
)
from app.grpc_clients.listener_grpc_exception_handler import grpc_listener_client_exception_handler

class ListenerClient:
    """ Клиент слушателя """
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('listener_web:50051')
        self.stub = ListenerServiceStub(self.channel)


    @grpc_listener_client_exception_handler
    async def get_listener(self, user_id: int):
        """ Получение данных слушателя """
        request = GetListenerRequest(user_id=user_id)
        response = await self.stub.GetListener(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def create_listener(
            self,
            user_id: int,
            first_name: str,
            last_name: str,
            birth_date: str,
        ):
        """ Создание слушателя """
        request = CreateListenerRequest(user_id=user_id, first_name=first_name, last_name=last_name, birth_date=birth_date)
        response = await self.stub.CreateListener(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def delete_listener(self, user_id: int):
        """ Удаление слушателя """
        request = DeleteListenerRequest(user_id=user_id)
        response = await self.stub.DeleteListener(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def like(self, user_id: int, track_id: int):
        """ Добавление или удаление лайка на трек"""
        request = LikeRequest(user_id=user_id, track_id=track_id)
        response = await self.stub.Like(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def interaction(self, user_id: int, track_id: int, listen_time: int, track_name: str, artist_id: int, artist_name: str, genre_id: int, genre_name: str):
        """ Добавление или обновление взаимодействия с треком """
        request = InteractionRequest(user_id=user_id, track_id=track_id, track_name=track_name, listen_time=listen_time, artist_id=artist_id, artist_name=artist_name, genre_id=genre_id, genre_name=genre_name)
        response = await self.stub.Interaction(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def history(self, user_id: int):
        """ Получение истории прослушиваний """
        request = HistoryRequest(user_id=user_id)
        response = await self.stub.History(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def create_playlist(self, user_id: int, title: str):
        """ Создание плейлиста """
        request = CreatePlaylistRequest(user_id=user_id, title=title)
        response = await self.stub.CreatePlaylist(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def delete_playlist(self, user_id: int, playlist_id: int):
        """ Удаление плейлиста """
        request = DeletePlaylistRequest(user_id=user_id, playlist_id=playlist_id)
        response = await self.stub.DeletePlaylist(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def get_all_playlists(self, user_id: int):
        """ Получение всех плейлистов слушателя """
        request = GetAllPlaylistsRequest(user_id=user_id)
        response = await self.stub.GetAllPlaylists(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def add_new_track_in_playlist(self, user_id: int, playlist_id: int, track_id: int):
        """ Добавление нового трека в плейлист """
        request = AddNewTrackInPlaylistRequest(user_id=user_id, playlist_id=playlist_id, track_id=track_id)
        response = await self.stub.AddNewTrackInPlaylist(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def delete_track_from_playlist(self, user_id: int, playlist_id: int, track_id: int):
        """ Удаление трека из плейлиста """
        request = DeleteTrackFromPlaylistRequest(user_id=user_id, playlist_id=playlist_id, track_id=track_id)
        response = await self.stub.DeleteTrackFromPlaylist(request)
        return response
    
    @grpc_listener_client_exception_handler
    async def get_all_tracks_in_playlist(self, user_id: int, playlist_id: int):
        """ Получение всех треков в плейлисте """
        request = GetAllTracksInPlaylistRequest(user_id=user_id, playlist_id=playlist_id)
        response = await self.stub.GetAllTracksInPlaylist(request)
        return response
