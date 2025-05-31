from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.logging import LOGGING, logger
from app.core.config import settings

from app.api.v1.artists_routers import router as artists_router
from app.api.v1.listener_routers import router as listener_router
from app.api.v1.albums_and_tracks import router as writer_router
from app.api.v1.auth_routers import router as auth_router
from app.api.exception_handlers import domain_exception_handler
from app.domain_exceptions.domain_exception import DomainException


@asynccontextmanager
async def lifespan(_: FastAPI):
    """ тут редис прокидывать """
    logger.info("start app")
    # await start_mapping()

    yield
    logger.info("finish app")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    default_response_class=JSONResponse,
    lifespan=lifespan,
)


app.add_exception_handler(DomainException, domain_exception_handler)

app.include_router(artists_router, prefix="/api/v1/artists", tags=["Исполнители"])
app.include_router(listener_router, prefix="/api/v1/listener", tags=["Слушатели"])
app.include_router(writer_router, prefix="/api/v1/writer", tags=["Writer"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING)
