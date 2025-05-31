""" Отлавливание всех типов исключений """
import grpc
from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

def grpc_exception_handler(func):
    """ Декоратор для отлавливания исключений """
    @wraps(func)
    async def wrapper(self, request, context):
        try:
            return await func(self, request, context)
        except HTTPException as e:
            if e.status_code == status.HTTP_409_CONFLICT:
                context.set_code(grpc.StatusCode.NOT_FOUND)
            elif e.status_code == status.HTTP_401_UNAUTHORIZED:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(e.detail)
        except SQLAlchemyError as e:
            context.set_code(grpc.StatusCode.ABORTED)
            context.set_details("Ошибка подключения к серверу")
        except Exception as e:
            await context.abort(grpc.StatusCode.UNKNOWN, f"Unexpected error: {str(e)}")

    return wrapper
