""" Клиент gRPC для взаимодействия с сервером писателя """

import grpc
from datetime import datetime, time
from app.grpc_clients.writer_pb2_grpc import WriterServiceStub
from app.grpc_clients.writer_pb2 import (
    CreateAlbum_Request,
    RemoveAlbum_Request,
    RemoveAlbumsByOwnerID_Request,
    CreateTrack_Request,
    RemoveTrack_Request
)
from app.schemas.track_meta_data import TrackCreate, AlbumCreate
from app.grpc_clients.writer_grpc_exception_handler import grpc_client_exception_handler

class WriterClient:
    """ gRPC клиент писателя """
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('writer_service:50051')
        self.stub = WriterServiceStub(self.channel)

    @grpc_client_exception_handler
    async def create_album(self, album: AlbumCreate):
        request = CreateAlbum_Request(
            title=album.title,
            owner_id=album.owner_id,
            release_date=datetime.combine(album.release_date, time.min),
        )
        response = await self.stub.CreateAlbum(request)
        return response.album_id
    
    @grpc_client_exception_handler
    async def remove_album(self, album_id: int):
        request = RemoveAlbum_Request(album_id=album_id)
        response = await self.stub.RemoveAlbum(request)
        return response.album_id

    @grpc_client_exception_handler
    async def remove_albums_by_owner_id(self, owner_id: int):
        request = RemoveAlbumsByOwnerID_Request(owner_id=owner_id)
        response = await self.stub.RemoveAlbumsByOwnerID(request)
        return list(response.album_ids)

    @grpc_client_exception_handler
    async def create_track(self, track: TrackCreate):
        request = CreateTrack_Request(
            title=track.title,
            album_id=track.album_id,
            explicit=track.explicit,
            genre_names=track.genre_names
        )
        response = await self.stub.CreateTrack(request)
        return response.track_id

    @grpc_client_exception_handler
    async def remove_track(self, track_id: int):
        request = RemoveTrack_Request(
            track_id=track_id
        )
        response = await self.stub.RemoveTrack(request)
        return response.track_id
