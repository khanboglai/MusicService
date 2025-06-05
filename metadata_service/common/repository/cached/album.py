import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional

import redis.asyncio as redis

from src.common.core.logging import logger
from src.common.models.album import Album
from src.common.repository.abstract.album import AlbumRepositoryABC
from src.common.exceptions import *


class CachedAlbumRepository(AlbumRepositoryABC):
    """ Основной репозиторий альбомов (с поддержкой Redis) """
    
    def __init__(self, repo: AlbumRepositoryABC, redis: redis.Redis):
        self.repo = repo
        self.redis = redis

    async def create_album(self, album: Album) -> Album:
        return await self.repo.create_album(album)

    async def get_album_by_id(self, id: int) -> Optional[Album]:
        cache_key = f"album_{id}"
        cached = await self.redis.get(cache_key)
        if cached:
            logger.info(f"Данные об альбоме с {id} взяты из Redis")
            data = json.loads(cached)
            return Album(**data)

        album = await self.repo.get_album_by_id(id)
        if album:
            await self.redis.setex(cache_key, 300, json.dumps(album.to_json()))
            logger.info(f"Данные об исполнителе {album.title} записаны в Redis")

        return album
    
    async def get_albums_by_owner_id(self, owner_id: int) -> list[Album]:
        return await self.repo.get_albums_by_owner_id(owner_id)
    
    async def get_all_albums(self) -> list[Album]:
        return await self.repo.get_all_albums()

    async def remove_album(self, album_id: int) -> int:
        return await self.repo.remove_album(album_id)

    async def remove_albums_by_owner_id(self, owner_id: int) -> list[int]:
        return await self.repo.remove_albums_by_owner_id(owner_id)
