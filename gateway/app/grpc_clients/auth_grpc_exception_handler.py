from functools import wraps
import grpc
from grpc import StatusCode
from grpc.aio import AioRpcError

from app.domain_exceptions.auth_exceptions import *


def grpc_auth_client_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                if "не найдено" in e.details().lower():
                    raise UserExistanceException(e.details())
                elif "существует" in e.details().lower():
                    raise UniqueUserException(e.details())
            elif e.code() == grpc.StatusCode.UNAUTHENTICATED:
                if "неправильный" in e.details().lower():
                    raise InvalidLoginPasswordException(e.details())
                elif "отсутствует" in e.details().lower():
                    raise TokenExistanceException(e.details())
                elif "данные" in e.details().lower():
                    raise IncorrectTokenDataException(e.details())
                elif "срок" in e.details().lower():
                    raise ExpiredTokenException(e.details())
                elif "не существует" in e.details().lower():
                    raise UserExistanceException(e.details())
                elif "повреждён" in e.details().lower():
                    raise DamagedTokenException(e.details())
            elif e.code() == grpc.StatusCode.ABORTED:
                raise SQLConnectException(e.details())
            else:
                raise ValueError(e.details(), e.code())
    
    return wrapper