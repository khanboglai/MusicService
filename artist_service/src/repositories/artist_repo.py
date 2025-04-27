from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.artist import Artist
from domain_repo import ArtistRepositoryAbc


class ArtistRepository(ArtistRepositoryAbc):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_artist(self, artist_id: int) -> Artist:
        ...