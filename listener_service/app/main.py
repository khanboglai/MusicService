from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
import asyncio

from database.models import start_mapping
# from dependencies.main import setup_dependencies
from core.config import logger
from database.repository.abc.listener import BaseListenerRepo
from database.repository.abc.like import BaseLikeRepo
from database.repository.abc.interaction import BaseInteractionRepo
from domain.entities.real.listener import Listener
from domain.values.real.age import Age
from domain.values.real.name import Name
from domain.exceptions.abc.base import AplicationException
from database.exceptions.abc.base import (
    DatabaseException,
    DatabaseErrorException
)
from grpcc.server import serve


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Application started!")
    await start_mapping()
    logger.info("Data mapped!")
    asyncio.create_task(serve())
    logger.info("GRPC Started")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    lifespan=lifespan,
)

# deps = setup_dependencies(app)
# for interfece, _ in deps.items():
#     logger.info(f"DEPENDENCY: {interfece}")
# logger.info("Dependencies set up!")


@app.get("/")
async def root():
    return {"message": "Hello world!"}

# GRPC
# @app.post("/listener/add")
# async def create_listener(
#         user_id: int, # временно, потом будем получать из куки
#         first_name: str,
#         last_name: str,
#         birth_date: str,
#         listener_repository: BaseListenerRepo = Depends()
#     ):
#     try:
#         new_listener = Listener(user_id, Name(first_name), Name(last_name), Age(birth_date))
#         listener = await listener_repository.insert_listener(listener=new_listener)
#         return {"id": listener.oid, "user_id": listener.user_id, "first_name": listener.firstname, "last_name": listener.lastname}
#     except AplicationException as e:
#         raise HTTPException(status_code=422, detail=e.message)
#     except DatabaseException as e:
#         raise HTTPException(status_code=423, detail=e.message)
#     except DatabaseErrorException as e:
#         raise HTTPException(status_code=500, detail=e.message)

# # GRPC
# @app.get("/listener/get")
# async def read_listener(
#         user_id: int,
#         listener_repository: BaseListenerRepo = Depends()
#     ):
#     try:
#         listener = await listener_repository.get_listener_by_user_id(user_id=user_id)
#         if listener:
#             return {"id": listener.oid, "user_id": listener.user_id, "first_name": listener.firstname, "last_name": listener.lastname}
#     except DatabaseException as e:
#         raise HTTPException(status_code=423, detail=e.message)
#     except DatabaseErrorException as e:
#         raise HTTPException(status_code=500, detail=e.message)
    
# @app.delete("/listener/delete")
# async def delete_listener(
#         user_id: int, # временно, потом будем получать из куки
#         listener_repository: BaseListenerRepo = Depends()
#     ):
#     try:
#         await listener_repository.delete_listener(user_id=user_id)
#         return {"message": "Deleted successfully"}
#     except DatabaseException as e:
#         raise HTTPException(status_code=423, detail=e.message)
#     except DatabaseErrorException as e:
#         raise HTTPException(status_code=500, detail=e.message)
    
# @app.post("/like")
# async def add_del_like(
#         user_id: int,
#         track_id: int,
#         like_repository: BaseLikeRepo = Depends(),
#         listener_repository: BaseListenerRepo = Depends()
#     ):
#     try:
#         listener = await listener_repository.get_listener_by_user_id(user_id=user_id)
#         like = await like_repository.add_or_delete_like(listener=listener, track_id=track_id)
#         if like:
#             return {"id": like.event_id, "listener": like.user, "track_id": like.track_id}
#     except DatabaseException as e:
#         raise HTTPException(status_code=423, detail=e.message)
#     except DatabaseErrorException as e:
#         raise HTTPException(status_code=500, detail=e.message)
    
# @app.post("/interaction")
# async def add_upd_interaction(
#         user_id: int,
#         track_id: int,
#         listen_time: int,
#         interaction_repository: BaseInteractionRepo = Depends(),
#         listener_repository: BaseListenerRepo = Depends()
#     ):
#     try:
#         listener = await listener_repository.get_listener_by_user_id(user_id=user_id)
#         interaction = await interaction_repository.add_or_update_interaction(
#             listener=listener,
#             track_id=track_id, 
#             listen_time=listen_time
#         )
#         return interaction
#     except DatabaseException as e:
#         raise HTTPException(status_code=423, detail=e.message)
#     except DatabaseErrorException as e:
#         raise HTTPException(status_code=500, detail=e.message)

