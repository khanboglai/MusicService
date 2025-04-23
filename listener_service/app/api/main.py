from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from uuid import UUID

from infra.database.models import start_mapping
from infra.database.repository.listener_repository import ListenerRepository

# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     start_mapping()


app = FastAPI()
listener_repository = ListenerRepository()

@app.on_event("startup")
async def startup_event():
    await start_mapping()

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.post("/listeners/")
async def create_listener(first_name: str, last_name: str, birth_date: str):
    listener = await listener_repository.add_listener(first_name, last_name, birth_date)
    return {"id": listener.oid, "first_name": listener.first_name, "last_name": listener.last_name}

@app.get("/listeners/{listener_id}")
async def read_listener(listener_id: UUID):
    listener = await listener_repository.get_listener_by_id(listener_id)
    if listener:
        await {"id": listener.oid, "first_name": listener.first_name, "last_name": listener.last_name}
    raise HTTPException(status_code=404, detail="Listener not found")

@app.on_event("shutdown")
async def shutdown_event():
    await listener_repository.close()
