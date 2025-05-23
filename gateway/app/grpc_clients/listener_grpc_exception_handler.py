from functools import wraps
import grpc
from grpc import StatusCode
from grpc.aio import AioRpcError

from app.domain_exceptions.listener_exceptions import *


def grpc_listener_client_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AioRpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                if "greater" in e.details().lower():
                    raise AgeTooSmallException(e.details())
                elif "smaller" in e.details().lower():
                    raise AgeTooBigException(e.details())
                elif "format" in e.details().lower():
                    raise AgeIncorrectFormat(e.details())
                elif "long" in e.details().lower():
                    raise NameTooLongException(e.details())
                elif "empty" in e.details().lower():
                    raise EmptyNameException(e.details())
                elif "chars" in e.details().lower():
                    raise NotRealNameException(e.details())
            elif e.code() == StatusCode.UNAVAILABLE:
                if "exists" in e.details().lower():
                    raise NotExistException(e.details())
                elif "unique" in e.details().lower():
                    raise UniqueException(e.details())
            else:
                raise ValueError(e.details(), e.code())
    
    return wrapper