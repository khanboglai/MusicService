import grpc
from functools import wraps

from database.exceptions.abc.base import DatabaseErrorException, DatabaseException
from domain.exceptions.abc.base import AplicationException


def grpc_exception_handler(func):
    @wraps(func)
    async def wrapper(self, request, context):
        try:
            return await func(self, request, context)
        except DatabaseErrorException as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(e.message)
        except DatabaseException as e:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details(e.message)
        except AplicationException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.message)

    return wrapper
