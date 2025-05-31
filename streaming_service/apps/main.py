import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from apps.core.logging import LOGGING, logger
from apps.core.config import settings
# from src.api.exception_handlers import domain_exception_handler
# from src.domain_exceptions.domain_exception import DomainException
from apps.grpc.server import serve


@asynccontextmanager
async def lifespan(_: FastAPI):
    """ тут редис прокидывать """
    logger.info("start apps")
    asyncio.create_task(serve())
    logger.info("gRPC server start")

    yield
    # await redis_client.close()
    logger.info("finish apps")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


# apps.add_exception_handler(DomainException, domain_exception_handler)

@app.get("/")
async def straming_service():
    return {"message": "stramming service"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING)
