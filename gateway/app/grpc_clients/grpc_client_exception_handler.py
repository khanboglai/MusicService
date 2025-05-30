from functools import wraps
import grpc
from grpc import StatusCode
from grpc.aio import AioRpcError
from app.domain_exceptions import UniqueViolationException, InvalidIdException, InvalidDescriptionSize
from app.core.logging import logger


def grpc_client_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AioRpcError as e:
            logger.error(f"gRPC error caught: code={e.code()}, details={e.details()}")
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise UniqueViolationException(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise InvalidIdException(e.details())
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise InvalidDescriptionSize(e.details())
            else:
                logger.error(f"Unhandled gRPC error: code={e.code()}, details={e.details()}")
                raise ValueError(e.details(), e.code())
    return wrapper