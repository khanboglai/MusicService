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