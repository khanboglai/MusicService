from datetime import datetime
import grpc
import asyncio
from concurrent import futures
from google.protobuf.empty_pb2 import Empty

from domain.entities.real.listener import Listener
from domain.events.real.interaction import NewInteractionRegistered
from domain.events.real.like import NewLikeRegistered
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
)
from domain.values.real.age import Age
from domain.values.real.name import Name
from core.config import logger


class ListenerService:
    def __init__(self, listener_repo, like_repo, interaction_repo):
        self.listener_repo = listener_repo
        self.like_repo = like_repo
        self.interaction_repo = interaction_repo


    # @grpc_exception_handler
    async def GetListener(self, request, context):
        user_id = int(request.user_id)
        listener = await self.listener_repo.get_listener_by_user_id(user_id=user_id)
        logger.info(f"GRPC: Getting user data for listener with listener id {listener.oid}")
        return GetListenerResponse(listener_id=listener.oid, user_id=listener.user_id, first_name=listener.first_name, last_name=listener.last_name)
    
    # @grpc_exception_handler
    async def CreateListener(self, request, context):
        new_listener = Listener(
            user_id=int(request.user_id),
            firstname=Name(str(request.first_name)),
            lastname=Name(str(request.last_name)),
            birthdate=Age(str(request.birth_date))
        )
        listener = await self.listener_repo.insert_listener(listener=new_listener)
        return CreateListenerResponse(listener_id=listener.oid, user_id=listener.user_id, first_name=listener.first_name, last_name=listener.last_name)
    
    # @grpc_exception_handler
    async def DeleteListener(self, request, context):
        user_id = int(request.user_id)
        await self.listener_repo.delete_listener(user_id=user_id)
        return DeleteListenerResponse(delete_message=f"User with id {user_id} deleted successfully!")
    
    # @grpc_exception_handler
    async def Like(self, request, context):
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        like = await self.like_repo.add_or_delete_like(listener=listener, track_id=int(request.track_id))
        if like:
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
        return LikeResponse(
            deleted=Empty(),
        )
    
    # @grpc_exception_handler
    async def Interaction(self, request, context):
        listener = await self.listener_repo.get_listener_by_user_id(user_id=int(request.user_id))
        interaction = await self.interaction_repo.add_or_update_interaction(
            listener=listener,
            track_id=int(request.track_id),
            listen_time=int(request.listen_time),
        )
        # logger.debug(f"Value: {interaction.user.oid} type: {type(interaction.user.oid)}")
        logger.debug(f"{interaction}")
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