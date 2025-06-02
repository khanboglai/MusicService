from datetime import datetime
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.exc import IntegrityError
from common.repository.album import AlbumRepository
from common.repository.track import TrackRepository
from common.models.album import Album
from common.models.track import Track
from common.schemas.album import AlbumCreate
from common.schemas.track import TrackCreate
from common.exceptions import *


@pytest.mark.asyncio
async def test_create_album():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    repo = AlbumRepository(db=mock_db)

    new_album = Album(
        title="Test Album",
        owner_id=1,
        release_date=datetime.now(),
    )

    created_album = await repo.create_album(new_album)
    mock_db.add.assert_called_once_with(new_album)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(new_album)

    assert created_album == new_album

@pytest.mark.asyncio
async def test_create_track():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    repo = TrackRepository(db=mock_db)

    new_track = Album(
        title="Test Track",
        album_id=1,
        explicit=False,
    )

    genre_names = ["Pop", "Rock"]
    
    created_track = await repo.create_track(new_track)
    mock_db.add.assert_called_once_with(new_track)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(new_track)

    assert created_track == new_track

@pytest.mark.asyncio
async def test_delete_track():
    mock_db = AsyncMock()
    repo = TrackRepository(db=mock_db)

    track = Track(
        title="Test Track",
        album_id=1,
        explicit=False,
    )
    track.oid = 1

    repo.get_artist_by_id = AsyncMock(return_value=track)

    result = await repo.delete_track(track.oid)
    assert result == track.title

    repo.get_artist_by_id.assert_called_once_with(track.oid)
    mock_db.delete.assert_called_once_with(track)
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_album():
    mock_db = AsyncMock()
    repo = AlbumRepository(db=mock_db)

    album = Album(
        title="Test Artist",
        owner_id="test@example.com",
        release_date=None,
    )
    album.oid = 1

    repo.get_artist_by_id = AsyncMock(return_value=album)

    result = await repo.delete_album(album.oid)
    assert result == album.title

    repo.get_artist_by_id.assert_called_once_with(album.oid)
    mock_db.delete.assert_called_once_with(album)
    mock_db.commit.assert_called_once()
