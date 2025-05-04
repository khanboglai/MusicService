from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.domain_exceptions.domain_exception import DomainException


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
