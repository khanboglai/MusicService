from src.common.models.album import Album
from src.common.models.album import Track

from src.common.database.session import engine

from sqlalchemy import (
    Column,
    Date,
    Integer,
    Boolean,
    Table,
    Text,
    ForeignKey,
    String,
    )
from sqlalchemy.orm import column_property, registry, relationship


mapper_registry = registry()

class Genre:
    _name: str

    def __init__(self, name):
        self._name = name

genres_table = Table(
    "genres",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, unique=True, nullable=False),
)

albums_table = Table(
    "albums",
    mapper_registry.metadata,
    Column("oid", Integer, primary_key=True, autoincrement=True),
    Column("_title", String, nullable=False),
    Column("_owner_id", Integer, nullable=False),
    Column("_release_date", Date, nullable=False),
)

tracks_table = Table(
    "tracks",
    mapper_registry.metadata,
    Column("oid", Integer, primary_key=True, autoincrement=True),
    Column("_title", String, nullable=False),
    Column("_album_id", Integer, ForeignKey("albums.id")),
    Column("_explicit", Boolean),
)

track_genres_table = Table(
    "track_genres",
    mapper_registry.metadata,
    Column("track_id", Integer, ForeignKey("tracks.id")),
    Column("genre_id", Integer, ForeignKey("genres.id")),
)

async def start_mapping():
    mapper_registry.map_imperatively(Genre, genres_table)

    mapper_registry.map_imperatively(
        Album,
        albums_table,
        properties={
            "tracks": relationship("Track", back_populates="album")
        }
    )

    mapper_registry.map_imperatively(
        Track,
        tracks_table,
        properties={
            "album": relationship("Album", back_populates="tracks"),
            "genres": relationship(
                Genre,
                secondary=track_genres_table,
                backref="tracks"
            )
        }
    )

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)