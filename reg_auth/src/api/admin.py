from fastapi import APIRouter, HTTPException, status, Form, Request, Depends, Response
from pydantic import BaseModel, Field, ValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from src.db.models import RoleEnum
from src.schemas.user import UserLogin
from src.db.requests import get_user, delete_user
from src.utils import validate_password, encode_jwt, get_access_token_lifetime, get_refresh_token_lifetime

router = APIRouter(prefix='/admin', tags=['Admin'])

@router.post("/delete_user")
async def register_user(user_login: str):
    try:
        existing_user = await delete_user(user_login)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователя с таким логином не найдено"
            )

        return {"message": "Пользователь был успешно удален"}

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ошибка подключения к серверу"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Непредвиденная ошибка: {str(e)}"
        )