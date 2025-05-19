from functools import wraps
import grpc
from grpc import StatusCode
from grpc.aio import AioRpcError
from app.domain_exceptions import UniqueViolationException, InvalidIdException


def grpc_client_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AioRpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise UniqueViolationException(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise InvalidIdException(e.details())
            else:
                raise ValueError(e.details(), e.code())
    return wrapper