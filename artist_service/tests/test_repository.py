from datetime import datetime
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.repositories.artist_repo import ArtistRepository
from src.models.artist import Artist
from src.value_objects.artist_description import Description


@pytest.mark.asyncio
async def test_create_artist():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    repo = ArtistRepository(db=mock_db)

    new_artist = Artist(
        name="Test Artist",
        email="fakemail@gmail.com",
        registered_at=datetime.now(),
        cover_path="Test.png",
        description=Description("Test Artist")
    )

    created_artist = await repo.create_artist(new_artist)
    mock_db.add.assert_called_once_with(new_artist)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(new_artist)

    assert created_artist == new_artist
