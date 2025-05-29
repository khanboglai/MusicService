import json
from typing import Optional

from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryABC
import redis.asyncio as redis


class CachedArtistRepo(ArtistRepositoryABC):
    def __init__(self, repo: ArtistRepositoryABC, redis: redis.Redis) -> None:
        self.repo = repo
        self.redis = redis

    async def create_artist(self, artist: Artist) -> Artist:
        return await self.repo.create_artist(artist)

    async def get_artist_by_id(self, artist_id: int) -> Artist:
        return await self.repo.get_artist_by_id(artist_id)

    async def get_artist_by_user_id(self, user_id: int) -> Optional[Artist]:
        cache_key = f"artist_{user_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            return Artist(**data)

        artist = await self.repo.get_artist_by_user_id(user_id)
        if artist:
            await self.redis.setex(cache_key, 300, artist.json())

        return artist

    async def delete_artist(self, artist_id: int):
        return await self.repo.delete_artist(artist_id)
