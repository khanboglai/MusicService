""" Определение обработчика кастомных исключений приложения """

from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.domain_exceptions.domain_exception import DomainException


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """ Кастомный обработчик исключений для fastapi приложения """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
