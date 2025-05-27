""" Серверная часть сервиса слушаетеля """
import grpc
import asyncio
from concurrent import futures
from google.protobuf.empty_pb2 import Empty

from domain.entities.real.listener import Listener
from dependencies.listener import ListenerRepositoryFactory
from dependencies.like import LikeRepositoryFactory
from dependencies.interaction import InteractionRepositoryFactory
from dependencies.playlist import PlaylistRepositoryFactory
from database.connect import get_db_session
from grpcc.listener_pb2_grpc import add_ListenerServiceServicer_to_server
from grpcc.listener_pb2 import (
    GetListenerResponse,
    CreateListenerResponse,
    DeleteListenerResponse,
    ListenerResponse,
    LikeResponse,
    LikeData,
    InteractionResponse,
    InteractionsHistoryResponse,
    HistoryResponse,
    PlaylistResponse,
    DeletePlaylistResponse,
    GetAllPlaylistsResponse,
    TrackInPlaylistResponse,
    DeleteTrackFromPlaylistResponse,
    GetAllTracksInPlaylistResponse,
)
from domain.values.real.age import Age
from domain.values.real.name import Name
from core.config import logger
from grpcc.grpc_exceptions import grpc_exception_handler


class ListenerService:
    """ Сервис слушателя """
    def __init__(self, listener_repo, like_repo, interaction_repo, playlist_repo):
        self.listener_repo = listener_repo
        self.like_repo = like_repo
        self.interaction_repo = interaction_repo
        self.playlist_repo = playlist_repo


    @grpc_exception_handler
    async def GetListener(self, request, context):
        """ Ручка для получения слушателя по user_id (все поля) """
        user_id = int(request.user_id)
        listener = await self.listener_repo.get_listener_by_user_id(user_id=user_id)
        logger.info(f"GRPC: Getting user data for listener with listener id {listener.oid}")
        return GetListenerResponse(listener_id=listener.oid, user_id=listener.user_id, first_name=listener.first_name, last_name=listener.last_name)
    
    @grpc_exception_handler
    async def CreateListener(self, request, context):
        """ Ручка для создания нового слушателя """
        new_listener = Listener(
            user_id=int(request.user_id),
            firstname=Name(str(request.first_name)),
            lastname=Name(str(request.last_name)),
            birthdate=Age(str(request.birth_date))
        )
        listener = await self.listener_repo.insert_listener(listener=new_listener)
        _ = await self.playlist_repo.insert_playlist(listener=listener, title="liked")
        logger.info(f"GRPC: Listener with listener_id: {listener.oid}, user_id: {listener.user_id} and name {listener.first_name} {listener.last_name} was created!")
        return CreateListenerResponse(listener_id=listener.oid, user_id=listener.user_id, first_name=listener.first_name, last_name=listener.last_name)
    
    @grpc_exception_handler
    async def DeleteListener(self, request, context):
        """ Ручка для удаления слушателя по user_id """
        user_id = int(request.user_id)
        await self.listener_repo.delete_listener(user_id=user_id)
        logger.info(f"GRPC: Listener with user_id {user_id} was deleted!")
        return DeleteListenerResponse(delete_message=f"User with id {user_id} deleted successfully!")
    
    @grpc_exception_handler
    async def Like(self, request, context):
        """ Ручка для поставки или удаления лайка """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        like = await self.like_repo.add_or_delete_like(listener=listener, track_id=int(request.track_id))
        liked_playlist = await self.playlist_repo.get_playlist_by_title(title="liked", listener=listener)
        if like:
            _ = await self.playlist_repo.add_new_track_in_playlist(listener=listener, playlist_id=liked_playlist.event_id, track_id=int(request.track_id), from_user=False)
            logger.info(f"GRPC: Like from listener with listener_id: {like.user.oid}, user_id: {like.user.user_id} and name {like.user.first_name} {like.user.last_name} on track with track_id {like.track_id} was set!")
            return LikeResponse(
                liked=LikeData(
                    id=like.event_id,
                    track_id=like.track_id,
                    listener=ListenerResponse(
                        listener_id=like.user.oid,
                        user_id=like.user.user_id,
                        first_name=like.user.first_name,
                        last_name=like.user.last_name,
                        birth_date=str(like.user.birth_date),
                        subscription=like.user.subscription,
                    ),
                ),
            )
        
        _ = await self.playlist_repo.delete_track_from_playlist(listener=listener, playlist_id=liked_playlist.event_id, track_id=int(request.track_id), from_user=False)
        logger.info(f"GRPC: Like from listener with listener_id: {listener.oid}, user_id: {listener.user_id} and name {listener.first_name} {listener.last_name} on track with track_id {int(request.track_id)} was deleted!")
        return LikeResponse(
            deleted=Empty(),
        )
    
    @grpc_exception_handler
    async def Interaction(self, request, context):
        """ Ручка для добавления или обновления взаимодействия """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        interaction = await self.interaction_repo.add_or_update_interaction(
            listener=listener,
            track_id=int(request.track_id),
            listen_time=int(request.listen_time),
            track_name=str(request.track_name),
            artist_id=int(request.artist_id),
            artist_name=str(request.artist_name),
            genre_id=int(request.genre_id),
            genre_name=str(request.genre_name)
        )
        logger.info(f"GRPC: Interaction from listener with listener_id: {interaction.user.oid}, user_id: {interaction.user.user_id} and name {interaction.user.first_name} {interaction.user.last_name} on track with track_id {interaction.track_id} was registered on {interaction.listen_time} seconds was registered!")
        return InteractionResponse(
            listener=ListenerResponse(
                listener_id=interaction.user.oid,
                user_id=interaction.user.user_id,
                first_name=interaction.user.first_name,
                last_name=interaction.user.last_name,
                birth_date=str(interaction.user.birth_date),
                subscription=interaction.user.subscription,
            ),
            track_id=interaction.track_id,
            listen_time=interaction.listen_time,
        )
    
    @grpc_exception_handler
    async def History(self, request, context):
        """ Ручка для выгрузки истории слушателя по user_id (сначала новые) """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        interactions = await self.interaction_repo.get_listener_history(listener=listener)
        logger.info(f"GRPC: History for listener with listener_id: {listener.oid}, user_id: {listener.user_id} and name {listener.first_name} {listener.last_name} was loaded!")
        return HistoryResponse(
            listener=ListenerResponse(
                listener_id=listener.oid,
                user_id=listener.user_id,
                first_name=listener.first_name,
                last_name=listener.last_name,
                birth_date=str(listener.birth_date),
                subscription=listener.subscription,
            ),
            interactions=[InteractionsHistoryResponse(track_id=interaction.track_id, last_interaction=str(interaction.last_interaction)) for interaction in interactions],
        )
    
    @grpc_exception_handler
    async def CreatePlaylist(self, request, conext):
        """ Ручка создания плейлиста """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        playlist = await self.playlist_repo.insert_playlist(listener=listener, title=str(request.title))
        logger.info(f"GRPC: Playlist with playlist_id {playlist.event_id} was created by user with user_id {int(request.user_id)}")
        return PlaylistResponse(playlist_id=playlist.event_id, title=playlist.title)
    
    @grpc_exception_handler
    async def DeletePlaylist(self, request, context):
        """ Ручка удаления плейлиста """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        await self.playlist_repo.delete_playlist(listener=listener, playlist_id=int(request.playlist_id))
        logger.info(f"GRPC: Playlist with playlist_id {int(request.playlist_id)} was deleted by user with user_id {int(request.user_id)}")
        return DeletePlaylistResponse(delete_message = f"Playlist with playlist_id {int(request.playlist_id)} was deleted successfully!")
    
    @grpc_exception_handler
    async def GetAllPlaylists(self, request, context):
        """ Ручка получения всех плейлистов пользователя """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        playlists = await self.playlist_repo.get_all_playlists(listener=listener)
        logger.info(f"GRPC: Getting playlists of user with user_id {int(request.user_id)}")
        return GetAllPlaylistsResponse(
            listener=ListenerResponse(
                listener_id=listener.oid,
                user_id=listener.user_id,
                first_name=listener.first_name,
                last_name=listener.last_name,
                birth_date=str(listener.birth_date),
                subscription=listener.subscription,
            ),
            playlists=[PlaylistResponse(playlist_id=playlist.event_id, title=playlist.title) for playlist in playlists],
        )
    
    @grpc_exception_handler
    async def AddNewTrackInPlaylist(self, request, context):
        """ Ручка добавления трека в плейлист """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        track = await self.playlist_repo.add_new_track_in_playlist(listener=listener, playlist_id=int(request.playlist_id), track_id=int(request.track_id))
        logger.info(f"GRPC: Track with track_id {int(request.track_id)} was added in playlist with playlist_id {int(request.playlist_id)} by user with user_id {int(request.user_id)}")
        return TrackInPlaylistResponse(playlist_id=int(request.playlist_id), track_id=int(request.track_id))
    
    @grpc_exception_handler
    async def DeleteTrackFromPlaylist(self, request, context):
        """ Ручка удаления трека из плейлиста """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        await self.playlist_repo.delete_track_from_playlist(listener=listener, playlist_id=int(request.playlist_id), track_id=int(request.track_id))
        logger.info(f"GRPC: Track with track_id {int(request.track_id)} was deleted from playlist with playlist_id {int(request.playlist_id)} by user with user_id {int(request.user_id)}")
        return DeleteTrackFromPlaylistResponse(delete_message=f"Track with track_id {int(request.track_id)} was deleted from playlist with playlist_id {int(request.playlist_id)} successfully!")

    @grpc_exception_handler
    async def GetAllTracksInPlaylist(self, request, context):
        """ Ручка получения всех треков в плейлисте """
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        tracks = await self.playlist_repo.get_tracks_in_playlist(listener=listener, playlist_id=int(request.playlist_id))
        logger.info(f"GRPC: Getting tracks from playlist with playlist_id {int(request.playlist_id)}")
        return GetAllTracksInPlaylistResponse(
            tracks=[TrackInPlaylistResponse(playlist_id=track.playlist_id, track_id=track.track_id) for track in tracks],
        )

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    async with get_db_session() as db:
        # repo = await ArtistRepositoryFactory.create(
        #     db=db,
        #     use_cache=True,
        #     redis_client=redis_client
        # )
        listener_repo = await ListenerRepositoryFactory.create(db)
        like_repo = await LikeRepositoryFactory.create(db)
        interaction_repo = await InteractionRepositoryFactory.create(db)
        playlist_repo = await PlaylistRepositoryFactory.create(db)

    service = ListenerService(
        listener_repo=listener_repo,
        like_repo=like_repo,
        interaction_repo=interaction_repo,
        playlist_repo=playlist_repo,
    )

    add_ListenerServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())