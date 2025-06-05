""" Ручки клиента сервиса регистрации и аутентификации """
import os

from fastapi import APIRouter, HTTPException, Request, Response, Depends

from app.grpc_clients.artist_client import ArtistClient
from app.grpc_clients.auth_client import AuthClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType
from app.grpc_clients.listener_client import ListenerClient
from app.schemas.role_enum import RoleEnum


router = APIRouter()
auth_client = AuthClient()
artist_client = ArtistClient()
listener_client = ListenerClient()


async def get_current_user(request: Request, response: Response):
    """ Поучение пользователя из сервиса auth """
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token is None:
        access_token = ""
    if refresh_token is None:
        refresh_token = ""

    user = await auth_client.get_me(access_token, refresh_token)

    response.set_cookie(
        key="access_token",
        value=str(user.access_token),
        httponly=True,
    )
    return user


def check_role(required_role: str):
    async def wrapper(user = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail=f"Requires {required_role} role")
        return user
    return wrapper


@router.post('/login')
@handle_exceptions
async def login_user(login: str, password: str, request: Request, response: Response):
    tokens = await auth_client.login_user(login, password)
    
    # Устанавливаем куки
    response.set_cookie(
        key="access_token",
        value=str(tokens.access_token),
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=str(tokens.refresh_token),
        secure=True,
        httponly=True,
    )

    return {"message": "Welcome!"}

# эта ручка не идет на сервис регистрации, так как из за технических особенностей всю ответственность за куки взял на себя гейтвей
@router.delete('/logout')
@handle_exceptions
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Goodbye!"}

@router.get('/me')
@handle_exceptions
async def get_me(user = Depends(get_current_user)):
    """ Получение информации о текущем пользователе """
    return {
        "user_id": int(user.user_id),
        "login": str(user.login),
        "role": str(user.role),
    }


@router.post('/register')
@handle_exceptions
async def register_user(login: str, password: str, role: RoleEnum = RoleEnum.LISTNER):
    message = await auth_client.register_user(login, password, role.value)
    return {"message": str(message.message)}


@router.delete('/delete')
@handle_exceptions
async def delete_user(user = Depends(get_current_user)):
    # удаление пользователя из сервисов
    if user.role == RoleEnum.LISTNER.value:
        await listener_client.delete_listener(user.user_id)
    elif user.role == RoleEnum.ARTIST.value:
        await artist_client.delete_artist(user.user_id)

    message = await auth_client.delete_user(user.login)
    return {"message": str(message.message)}
