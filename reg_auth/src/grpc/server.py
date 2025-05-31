""" Серверная часть сервиса слушаетеля """
import grpc
import asyncio
from concurrent import futures
from fastapi import HTTPException, status

from src.grpc.auth_pb2_grpc import add_AuthServiceServicer_to_server
from src.db.requests import get_user, delete_user, get_password, create_user
from src.schemas.user import UserLogin
from src.utils import validate_password, encode_jwt, get_access_token_lifetime, get_refresh_token_lifetime
from src.api.me import get_current_user
from src.grpc.auth_pb2 import (
    UserLoginResponse,
    GetMeResponse,
    UserRegisterResponse,
    UserDeleteResponse,
)
from src.grpc.grpc_exceptions import grpc_exception_handler
from src.db.enums import RoleEnum


class AuthService:
    """ Сервис регистрации и аутентификации """
    @grpc_exception_handler
    async def UserLogin(self, request, context):
        """ Ручка для входа пользователя """
        login = str(request.login)
        password = str(request.password)
        user = UserLogin(login=login, password=password)
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
        
        jwt_payload = {
            "sub": str(existing_user.id),
            "login": existing_user.login
        }

        access_token = encode_jwt(jwt_payload, get_access_token_lifetime())
        refresh_token = encode_jwt(jwt_payload, get_refresh_token_lifetime())

        return UserLoginResponse(access_token=access_token, refresh_token=refresh_token) # возвращаем токены, чтобы на гейтвее вписать их в куку
    
    @grpc_exception_handler
    async def GetMe(self, request, context):
        """ Ручка для получения иноформации о своем юзере """
        access_token = str(request.access_token)
        refresh_token = str(request.refresh_token)

        if access_token == "": # в протике муторно писать что потенциально поле может быть пустым, поэтому вот так
            access_token = None
        if refresh_token == "":
            refresh_token = None
        
        user, access_token = await get_current_user(access_token=access_token, refresh_token=refresh_token)

        return GetMeResponse(user_id=user.id, login=user.login, role=str(user.role), access_token=access_token) # возвращаем токены, чтобы на гейтвее вписать их в куку
    
    @grpc_exception_handler
    async def UserRegister(self, request, context):
        """ Ручка для регистрации нового пользователя """
        login = str(request.login)
        password = str(request.password)
        role = str(request.role)

        existing_user = await get_user(login)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь уже существует"
            )
        user = UserLogin(login=login, password=password)
        new_user = await create_user(login, password, RoleEnum(role))

        return UserRegisterResponse(message=f"Пользователь создан с user_id {new_user.id}")
    
    @grpc_exception_handler
    async def UserDelete(self, request, context):
        """ Ручка для удаления пользователя """
        login = str(request.login)

        existing_user = await delete_user(login)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователя с таким логином не найдено"
            )
        
        return UserDeleteResponse(message="Пользователь был успешно удален")


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    service = AuthService()

    add_AuthServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())