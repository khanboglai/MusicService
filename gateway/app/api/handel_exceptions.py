""" Реализация декоратора для обработки ошибок при работе с gRPC """

from functools import wraps
from fastapi import HTTPException
from app.domain_exceptions import *


def handle_exceptions(func):
    """ Декоратор для обработки исключений при работе с gRPC """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except InvalidIdException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except UniqueViolationException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            # Для неопознанных ошибок
            raise HTTPException(status_code=500, detail="Internal Server Error")
    return wrapper
