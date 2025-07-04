from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.common.exceptions.exceptions import DomainException


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """ Обработчик ошибок для HTTP API """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )