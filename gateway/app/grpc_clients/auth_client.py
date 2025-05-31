""" Клиент gRPC для взаимодействия с сервером регистрации и авторизации """
import grpc

from app.grpc_clients.auth_pb2_grpc import AuthServiceStub
from app.grpc_clients.auth_pb2 import (
    UserLoginRequest,
    GetMeRequest,
    UserRegisterRequest,
    UserDeleteRequest,
)
from app.grpc_clients.auth_grpc_exception_handler import grpc_auth_client_exception_handler

class AuthClient:
    """ Клиент сервиса регистрации и аутентификации """
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('auth_service_app:50051')
        self.stub = AuthServiceStub(self.channel)

    @grpc_auth_client_exception_handler
    async def login_user(self, login: str, password: str):
        """ Вход в аккаунт """
        request = UserLoginRequest(login=login, password=password)
        response = await self.stub.UserLogin(request)
        return response
    
    @grpc_auth_client_exception_handler
    async def get_me(self, access_token: str, refresh_token: str):
        """ Получение информации о текущем пользователе """
        request = GetMeRequest(access_token=access_token, refresh_token=refresh_token)
        response = await self.stub.GetMe(request)
        return response
    
    @grpc_auth_client_exception_handler
    async def register_user(self, login: str, password: str, role: str):
        """ Создание аккаунта """
        request = UserRegisterRequest(login=login, password=password, role=role)
        response = await self.stub.UserRegister(request)
        return response
    
    @grpc_auth_client_exception_handler
    async def delete_user(self, login: str):
        """ Удаление пользователя """
        request = UserDeleteRequest(login=login)
        response = await self.stub.UserDelete(request)
        return response
