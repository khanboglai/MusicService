""" Ручки клиента слушателя """
import os

from fastapi import APIRouter, HTTPException
from app.grpc_clients.listener_client import ListenerClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType


router = APIRouter()
listener_client = ListenerClient()


@router.get('/listener/get')
@handle_exceptions
async def read_listener(user_id: int):
    listener = await listener_client.get_listener(user_id)
    return {"message": f"{listener}"}

@router.post('/listener/add')
@handle_exceptions
async def add_listener(
        user_id: int, # временно, потом будем получать из куки
        first_name: str,
        last_name: str,
        birth_date: str,
    ):
    listener = await listener_client.create_listener(
            user_id,
            first_name,
            last_name,
            birth_date,
        )
    return {"message": f"{listener}"}

@router.delete('/listener/delete')
@handle_exceptions
async def erase_listener(user_id: int):
    message = await listener_client.delete_listener(user_id)
    return {"message": f"{message}"}

@router.post('/like')
@handle_exceptions
async def liking(user_id: int, track_id: int):
    like = await listener_client.like(user_id, track_id)
    return {"message": f"{like}"}

@router.post('/interaction')
@handle_exceptions
async def interacting(
        user_id: int, # временно
        track_id: int, # это останется здесь (тк на фронте когда мы нажимаем на кнопку трека, то с фронта на бэк идет айдишник)
        track_name: str, # перенесется в тело функции (запрос к сервису ридера)
        listen_time: int,
        artist_id: int, # перенесется в тело функции (запрос к сервису артиста)
        artist_name: str, # перенесется в тело функции (запрос к сервису артиста)
        genre_id: int, # перенесется в тело функции (запрос к сервису ридера)
        genre_name: str, # перенесется в тело функции (запрос к сервису ридера)
    ):
    interaction = await listener_client.interaction(user_id, track_id, listen_time, track_name, artist_id, artist_name, genre_id, genre_name)
    return {"message": f"{interaction}"}

@router.get('/history')
@handle_exceptions
async def load_history(user_id: int):
    history = await listener_client.history(user_id)
    return {"message": f"{history}"}
