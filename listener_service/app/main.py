import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from datetime import date

from infra.database.models import start_mapping
from dependencies.main import setup_dependencies
from infra.core.config import logger
from infra.database.repository.abc.listener import BaseListenerRepo
from domain.entities.real.listener import Listener
from domain.values.real.age import Age
from domain.values.real.name import Name


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

@app.post("/listeners/")
async def create_listener(
        first_name: str,
        last_name: str,
        birth_date: str,
        listener_repository: BaseListenerRepo = Depends()
    ):
    new_listener = Listener.add_listener(Name(first_name), Name(last_name), Age(date.fromisoformat(birth_date))) # Тут возможно надо будет обрабатывать исключения + преобразователь дат
    listener = await listener_repository.insert_listener(listener=new_listener)
    return {"id": listener.oid, "first_name": listener.firstname, "last_name": listener.lastname}

@app.get("/listeners/{listener_id}")
async def read_listener(
        listener_id: int,
        listener_repository: BaseListenerRepo = Depends()
    ):
    listener = await listener_repository.get_listener(listener_id=listener_id)
    if listener:
        return {"id": listener.oid, "first_name": listener.firstname, "last_name": listener.lastname}
    raise HTTPException(status_code=404, detail="Listener not found")
