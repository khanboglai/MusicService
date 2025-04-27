from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.logging import LOGGING, logger
from src.core.config import settings
from src.database.models import start_mapping


@asynccontextmanager
async def lifespan(_: FastAPI):
    """ тут редис прокидывать """
    logger.info("start app")
    await start_mapping()
    logger.info("mapping done")
    yield
    logger.info("finish app")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING)
