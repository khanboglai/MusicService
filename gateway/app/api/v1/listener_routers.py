import os

from fastapi import APIRouter, HTTPException
from app.grpc_clients.listener_client import ListenerClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType


router = APIRouter()
listener_client = ListenerClient()


@router.get('/listener/get')
@handle_exceptions
async def read_listener(listener_id: int):
    listener = await listener_client.get_listener(listener_id)
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
async def liking(listener_id: int, track_id: int):
    like = await listener_client.like(listener_id, track_id)
    return {"message": f"{like}"}

@router.post('/interaction')
@handle_exceptions
async def interaction(listener_id: int, track_id: int, listen_time: int):
    interaction = await listener_client.interaction(listener_id, track_id, listen_time)
    return {"message": f"{interaction}"}