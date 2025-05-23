import asyncio
from contextlib import asynccontextmanager

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.logging import LOGGING, logger
from src.core.config import settings
from src.database.models import start_mapping
from src.api.v1.artists import router as artists_router
from src.api.v1.albums_and_tracks import router as writer_router
from src.api.exception_handlers import domain_exception_handler
from src.domain_exceptions.domain_exception import DomainException
from src.grpc.server import serve


@asynccontextmanager
async def lifespan(_: FastAPI):
    """ тут редис прокидывать """
    logger.info("start app")
    await start_mapping()
    logger.info("mapping done")
    redis_client = redis.Redis(host="redis", port=6379, db=0)
    logger.info("redis client done")
    asyncio.create_task(serve(redis_client))
    logger.info("gRPC server start")

    yield
    await redis_client.close()
    logger.info("finish app")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.add_exception_handler(DomainException, domain_exception_handler)

app.include_router(artists_router, prefix="/api/v1/artists", tags=["Исполнители"])
app.include_router(writer_router, prefix="/api/v1/writer")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING)
