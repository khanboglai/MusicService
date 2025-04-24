import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from infra.database.models import start_mapping
from infra.database.repository.listener_repository import ListenerRepository
from infra.config import logger

# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     start_mapping()


app = FastAPI()
listener_repository = ListenerRepository()

@app.on_event("startup")
async def startup_event():
    await start_mapping()
    logger.info("Data mapped!")

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.post("/listeners/")
async def create_listener(first_name: str, last_name: str, birth_date: str):
    listener = await listener_repository.add_listener(first_name, last_name, birth_date)
    return {"id": listener.oid, "first_name": listener.firstname, "last_name": listener.lastname}

@app.get("/listeners/{listener_id}")
async def read_listener(listener_id: int):
    listener = await listener_repository.get_listener_by_id(listener_id)
    if listener:
        return {"id": listener.oid, "first_name": listener.firstname, "last_name": listener.lastname}
    raise HTTPException(status_code=404, detail="Listener not found")

@app.on_event("shutdown")
async def shutdown_event():
    await listener_repository.close()

# if __name__ == "__main__":
#     uvicorn.run(
#         "api.main:app",
#         host="0.0.0.0",
#         port=8000,
#         log_config=LOGGING,
#         log_level=logging.INFO,
#         reload=True
#     )
