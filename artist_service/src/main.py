from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from core.logging import LOGGING
from core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """ тут редис прокидывать """
    print("start up")
    yield
    print("shutdown")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING)
