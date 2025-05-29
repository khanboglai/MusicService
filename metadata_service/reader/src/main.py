import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.common.core.logging import LOGGING, logger
from src.config import settings
from src.common.database.models import start_mapping
from src.api.v1.album import router as album_router
from src.api.v1.track import router as track_router
from src.api.exception_handler import domain_exception_handler
from src.common.exceptions.exceptions import DomainException
from src.grpc.server import serve


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("start app")
    await start_mapping()
    logger.info("mapping done")
    asyncio.create_task(serve())
    logger.info("gRPC server start")

    yield
    logger.info("finish app")

app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.add_exception_handler(DomainException, domain_exception_handler)

app.include_router(album_router, prefix="/api/v1/album", tags=["Чтение метаданных альбомов"])
app.include_router(track_router, prefix="/api/v1/track", tags=["Чтение метаданных треков"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8802, log_config=LOGGING)
