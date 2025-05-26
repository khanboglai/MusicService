""" Клиент gRPC для взаимодействия с сераером ридера """
import grpc

from app.grpc_clients.reader_pb2_grpc import ReaderServiceStub
from app.grpc_clients.reader_pb2 import (
    GetTrackRequest,
    GetTracksInAlbumRequest,
    GetAlbumRequest,
    GetAlbumInArtistRequest,
    GetTrackGenreRequest,
    GetAllAlbumsRequest,
)
from app.grpc_clients.reader_grpc_exception_handler import grpc_reader_client_exception_handler
from app.core.logging import logger


class ReaderClient:
    """ Клиент ридера """
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('reader_service:50051')
        self.stub = ReaderServiceStub(self.channel)


    @grpc_reader_client_exception_handler
    async def get_track(self, track_id: int):
        """ Получение данных о треке """
        request = GetTrackRequest(track_id=track_id)
        response = await self.stub.GetTrack(request)
        return response
    
    @grpc_reader_client_exception_handler
    async def get_tracks_in_album(self, album_id: int):
        """ Получение треков в альбоме """
        request = GetTracksInAlbumRequest(album_id=album_id)
        response = await self.stub.GetTracksInAlbum(request)
        return response
    
    @grpc_reader_client_exception_handler
    async def get_album(self, album_id: int):
        """ Получение данных об альбоме """
        request = GetAlbumRequest(album_id=album_id)
        response = await self.stub.GetAlbum(request)
        return response
    
    @grpc_reader_client_exception_handler
    async def get_albums_in_artist(self, artist_id: int):
        """ Получение альбомов исполнителя """
        request = GetAlbumInArtistRequest(artist_id=artist_id)
        response = await self.stub.GetAlbumInArtist(request)
        return response
    
    @grpc_reader_client_exception_handler
    async def get_track_genre(self, track_id: int):
        """ Получение жанра трека """
        request = GetTrackGenreRequest(track_id=track_id)
        response = await self.stub.GetTrackGenre(request)
        return response
    
    @grpc_reader_client_exception_handler
    async def get_all_albums(self):
        """ Получение всех альбомов """
        request = GetAllAlbumsRequest()
        response = await self.stub.GetAllAlbums(request)
        return response
    