from functools import wraps
import grpc
from grpc import StatusCode
from grpc.aio import AioRpcError
from app.domain_exceptions.writer_exceptions import *


def grpc_client_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AioRpcError as e:
            if (e.code() == grpc.StatusCode.NOT_FOUND) and ("альбом" in e.details().lower()):
                raise NoSuchAlbumException(e.details())
            elif (e.code() == grpc.StatusCode.NOT_FOUND) and ("трек" in e.details().lower()):
                raise NoSuchTrackException(e.details())
            elif (e.code() == grpc.StatusCode.ALREADY_EXISTS) and ("альбом" in e.details().lower()):
                raise OwnerAlbumDublicateException(e.details())
            elif (e.code() == grpc.StatusCode.ALREADY_EXISTS) and ("трек" in e.details().lower()):
                raise AlbumTrackDublicateException(e.details())
            else:
                raise ValueError(e.details(), e.code())
    return wrapper