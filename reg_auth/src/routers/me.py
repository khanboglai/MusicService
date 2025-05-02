from fastapi import APIRouter, HTTPException, status, Form, Request, Depends, Response
from pydantic import BaseModel, Field, ValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from db.models import RoleEnum
from schemas.user import UserLogin
from db.requests import get_user, get_password
from utils import validate_password, encode_jwt, get_access_token_lifetime, get_refresh_token_lifetime, decode_jwt
from jwt import ExpiredSignatureError, InvalidTokenError

router = APIRouter(prefix='/me', tags=['Me'])


async def get_current_user(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Отсутствует access-токен. Необходима авторизация"
        )

    try:
        payload = decode_jwt(access_token)
        login = payload.get("sub")
        username = payload.get("login")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access-токен содержит некорректные данные."
            )

        user = await get_user(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователя не существует."
            )

        return user

    except ExpiredSignatureError:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Скрок действия токена истек. Необходима авторизация."
            )

        try:
            refresh_payload = decode_jwt(refresh_token)
            login = refresh_payload.get("sub")
            username = refresh_payload.get("login")
            if not login:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh-токен содержит недопустимые данные."
                )

            user = await get_user(username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Пользователь, указанный в refresh-токене, не существует."
                )

            new_token_payload = {
                "sub": login,
                "username": username
            }
            new_token = encode_jwt(new_token_payload, get_access_token_lifetime())

            response.set_cookie(
                key="access_token",
                value=new_token,
                httponly=True,
                samesite="lax"
            )

            return user

        except (ExpiredSignatureError, InvalidTokenError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Срок действия refresh-токена истёк или он недействителен. Необходима авторизация"
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access-токен повреждён или имеет недопустимую подпись."
        )

@router.get("/")
async def get_me(username = Depends(get_current_user)):
    return {
        "message": "Пользователь авторизован",
        "user_id": username}