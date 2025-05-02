from fastapi import APIRouter, HTTPException, status, Form, Request, Depends, Response
from pydantic import BaseModel, Field, ValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from db.models import RoleEnum
from schemas.user import UserLogin
from db.requests import get_user, get_password
from utils import validate_password, encode_jwt, get_access_token_lifetime, get_refresh_token_lifetime

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/login")
async def login_user(user: UserLogin, request: Request, response: Response):
    try:
        success = False
        existing_user = await get_user(user.login)
        if existing_user:
            hash_pass = await get_password(user.login)
            if validate_password(user.password, hash_pass):
                success = True
            
        if not success:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильный логин или пароль"
            )
        # print("existing_user =", existing_user)
        # print("type =", type(existing_user))

        jwt_payload = {
            "sub": existing_user.id,
            "login": existing_user.login
        }

        access_token = encode_jwt(jwt_payload, get_access_token_lifetime())
        refresh_token = encode_jwt(jwt_payload, get_refresh_token_lifetime())

        print(access_token)

        response.set_cookie(
            key="access_token",
            value= access_token,
            httponly=True,
            samesite="lax"
        )

        response.set_cookie(
            key="refresh_token",
            value= refresh_token,
            httponly=True,
            samesite="lax"
        )

        return {"message": "Успешный вход"}

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
    
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Выход из аккаунта"}