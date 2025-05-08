from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends

from database.models import start_mapping
from dependencies.main import setup_dependencies
from core.config import logger
from database.repository.abc.listener import BaseListenerRepo
from database.repository.abc.like import BaseLikeRepo
from domain.entities.real.listener import Listener
from domain.events.real.like import NewLikeRegistered
from domain.values.real.age import Age
from domain.values.real.name import Name
from domain.exceptions.abc.base import AplicationException
from database.exceptions.abc.base import (
    DatabaseException,
    DatabaseErrorException
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Application started!")
    await start_mapping()
    logger.info("Data mapped!")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    lifespan=lifespan,
)

deps = setup_dependencies(app)
for interfece, _ in deps.items():
    logger.info(f"DEPENDENCY: {interfece}")
logger.info("Dependencies set up!")


@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.post("/listener/add")
async def create_listener(
        user_id: int, # временно, потом будем получать из куки
        first_name: str,
        last_name: str,
        birth_date: str,
        listener_repository: BaseListenerRepo = Depends()
    ):
    try:
        new_listener = Listener(user_id, Name(first_name), Name(last_name), Age(birth_date))
        listener = await listener_repository.insert_listener(listener=new_listener)
        return {"id": listener.oid, "user_id": listener.user_id, "first_name": listener.firstname, "last_name": listener.lastname}
    except AplicationException as e:
        raise HTTPException(status_code=422, detail=e.message)
    except DatabaseException as e:
        raise HTTPException(status_code=423, detail=e.message)
    except DatabaseErrorException as e:
        raise HTTPException(status_code=500, detail=e.message)

@app.get("/listener/get")
async def read_listener(
        listener_id: int,
        listener_repository: BaseListenerRepo = Depends()
    ):
    try:
        listener = await listener_repository.get_listener(listener_id=listener_id)
        if listener:
            return {"id": listener.oid, "user_id": listener.user_id, "first_name": listener.firstname, "last_name": listener.lastname}
    except DatabaseException as e:
        raise HTTPException(status_code=423, detail=e.message)
    except DatabaseErrorException as e:
        raise HTTPException(status_code=500, detail=e.message)
    
@app.delete("/listener/delete")
async def delete_listener(
        user_id: int, # временно, потом будем получать из куки
        listener_repository: BaseListenerRepo = Depends()
    ):
    try:
        await listener_repository.delete_listener(user_id=user_id)
        return {"message": "Deleted successfully"}
    except DatabaseException as e:
        raise HTTPException(status_code=423, detail=e.message)
    except DatabaseErrorException as e:
        raise HTTPException(status_code=500, detail=e.message)
    
@app.post("/like/add")
async def add_like(
        listener_id: int,
        track_id: int,
        like_repository: BaseLikeRepo = Depends(),
        listener_repository: BaseListenerRepo = Depends()
    ):
    try:
        listener = await listener_repository.get_listener(listener_id=listener_id)
        new_like = NewLikeRegistered(listener_id=listener, track_id=track_id)
        like = await like_repository.add_like(like=new_like)
        return {"id": like.event_id, "listener": like.user, "track_id": like.track_id}
    except DatabaseException as e:
        raise HTTPException(status_code=423, detail=e.message)
    except DatabaseErrorException as e:
        raise HTTPException(status_code=500, detail=e.message)
    # Здесь надо по DDD закидывать ивент к сущности слушателя, но пока будем рассчитывать на бд

@app.delete("/like/delete")
async def delete_like(
        listener_id: int,
        track_id: int,
        like_repository: BaseLikeRepo = Depends(),
        listener_repository: BaseListenerRepo = Depends()
    ):
    try:
        listener = await listener_repository.get_listener(listener_id=listener_id)
        await like_repository.delete_like(listener=listener, track_id=track_id)
        return {"message": "Deleted successfully"}
    except DatabaseException as e:
        raise HTTPException(status_code=423, detail=e.message)
    except DatabaseErrorException as e:
        raise HTTPException(status_code=500, detail=e.message)
    # Здесь уже надо удалять ивент из сущности слушателя
