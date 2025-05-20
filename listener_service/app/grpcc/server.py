import grpc
import asyncio
from concurrent import futures
from google.protobuf.empty_pb2 import Empty

from domain.entities.real.listener import Listener
from database.repository.real.listener import ListenerRepository
from database.repository.real.interaction import InteractionRepository
from database.repository.real.like import LikeRepository
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
)
from domain.values.real.age import Age
from domain.values.real.name import Name
from core.config import logger
from grpcc.grpc_exceptions import grpc_exception_handler


class ListenerService:
    def __init__(self, listener_repo, like_repo, interaction_repo):
        self.listener_repo = listener_repo
        self.like_repo = like_repo
        self.interaction_repo = interaction_repo


    @grpc_exception_handler
    async def GetListener(self, request, context):
        user_id = int(request.user_id)
        listener = await self.listener_repo.get_listener_by_user_id(user_id=user_id)
        logger.info(f"GRPC: Getting user data for listener with listener id {listener.oid}")
        return GetListenerResponse(listener_id=listener.oid, user_id=listener.user_id, first_name=listener.first_name, last_name=listener.last_name)
    
    @grpc_exception_handler
    async def CreateListener(self, request, context):
        new_listener = Listener(
            user_id=int(request.user_id),
            firstname=Name(str(request.first_name)),
            lastname=Name(str(request.last_name)),
            birthdate=Age(str(request.birth_date))
        )
        listener = await self.listener_repo.insert_listener(listener=new_listener)
        logger.info(f"GRPC: Listener with listener_id: {listener.oid}, user_id: {listener.user_id} and name {listener.first_name} {listener.last_name} was created!")
        return CreateListenerResponse(listener_id=listener.oid, user_id=listener.user_id, first_name=listener.first_name, last_name=listener.last_name)
    
    @grpc_exception_handler
    async def DeleteListener(self, request, context):
        user_id = int(request.user_id)
        await self.listener_repo.delete_listener(user_id=user_id)
        logger.info(f"GRPC: Listener with user_id {user_id} was deleted!")
        return DeleteListenerResponse(delete_message=f"User with id {user_id} deleted successfully!")
    
    @grpc_exception_handler
    async def Like(self, request, context):
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        like = await self.like_repo.add_or_delete_like(listener=listener, track_id=int(request.track_id))
        if like:
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
        
        logger.info(f"GRPC: Like from listener with listener_id: {listener.oid}, user_id: {listener.user_id} and name {listener.first_name} {listener.last_name} on track with track_id {int(request.track_id)} was deleted!")
        return LikeResponse(
            deleted=Empty(),
        )
    
    @grpc_exception_handler
    async def Interaction(self, request, context):
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        interaction = await self.interaction_repo.add_or_update_interaction(
            listener=listener,
            track_id=int(request.track_id),
            listen_time=int(request.listen_time),
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


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    async with get_db_session() as db:
        # repo = await ArtistRepositoryFactory.create(
        #     db=db,
        #     use_cache=True,
        #     redis_client=redis_client
        # )
        listener_repo = ListenerRepository(db)
        like_repo = LikeRepository(db)
        interaction_repo = InteractionRepository(db)

    service = ListenerService(
        listener_repo=listener_repo,
        like_repo=like_repo,
        interaction_repo=interaction_repo
    )

    add_ListenerServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())