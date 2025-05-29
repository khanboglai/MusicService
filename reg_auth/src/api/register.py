from fastapi import APIRouter, HTTPException, status, Form, Request, Depends
from pydantic import BaseModel, Field, ValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from src.db.models import RoleEnum
from src.schemas.user import UserLogin
from src.db.requests import get_user, create_user

router = APIRouter(prefix='/register', tags=['Reg'])

@router.post("/")
# async def register_user(login: str, password: str, role: RoleEnum = RoleEnum.LISTNER):
async def register_user(user: UserLogin, role: RoleEnum = RoleEnum.LISTNER):
    try:
        existing_user = await get_user(user.login)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь уже существует"
            )

        new_user = await create_user(user.login, user.password, role)
        return {"message": "Пользователь создан", "user_id": new_user.id}

    except HTTPException as http_exc:
        raise http_exc

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