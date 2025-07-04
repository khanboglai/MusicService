from fastapi import APIRouter, HTTPException, status, Form, Request, Depends, Response
from pydantic import BaseModel, Field, ValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from src.db.models import RoleEnum
from src.schemas.user import UserLogin
from src.db.requests import get_user, get_password
from src.utils import validate_password, encode_jwt, get_access_token_lifetime, get_refresh_token_lifetime, decode_jwt
from jwt import ExpiredSignatureError, InvalidTokenError

router = APIRouter(prefix='/me', tags=['Me'])


async def get_current_user(access_token: str, refresh_token: str):
    # access_token = request.cookies.get("access_token")
    # refresh_token = request.cookies.get("refresh_token")

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
        # user = {user.id, user.login, user.role}

        return user, access_token

    except ExpiredSignatureError:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Срок действия токена истек. Необходима авторизация."
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
            # user = {user.id, user.login, user.role}


            new_token_payload = {
                "sub": login,
                "username": username
            }
            new_token = encode_jwt(new_token_payload, get_access_token_lifetime())

            # response.set_cookie(
            #     key="access_token",
            #     value=new_token,
            #     httponly=True,
            #     samesite="lax"
            # )

            return user, new_token

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
async def get_me(user = Depends(get_current_user)):
    return {
        "message": "Пользователь авторизован",
        "user_id": user.id,
        "user_login": user.login,
        "user_role": user.role}
