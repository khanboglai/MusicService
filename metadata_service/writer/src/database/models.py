from src.models.album import Album
from src.models.track import Track

from src.database.session import engine

from sqlalchemy import (
    Column,
    Date,
    Integer,
    Boolean,
    Table,
    Text,
    ForeignKey,
    )
from sqlalchemy.orm import column_property, registry, composite


mapper_registry = registry()

albums_table = Table(
    "albums",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", Text, nullable=False),
    Column("cover_path", Text),
    Column("release_date", Date, nullable=False),
    Column("author_id", Integer, nullable=False),
)

tracks_table = Table(
    "tracks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("album_id", Integer, ForeignKey("albums.id"), nullable=False),
    Column("file_path", Text, nullable=False),
    Column("explicit", Boolean, nullable=False),
)

async def start_mapping():
    mapper_registry.map_imperatively(
        Album,
        albums_table,
        properties={
            "oid": column_property(albums_table.c.id),
            "_title": column_property(albums_table.c.title),
            "_cover_path": column_property(albums_table.c.cover_path),
            "_release_date": column_property(albums_table.c.release_date),
            "_author_id": column_property(albums_table.c.author_id),
        },
    )

    mapper_registry.map_imperatively(
        Track,
        tracks_table,
        properties={
            "oid": column_property(tracks_table.c.id),
            "_title": column_property(tracks_table.c.title),
            "_album_id": column_property(tracks_table.c.album_id),
            "_file_path": column_property(tracks_table.c.file_path),
            "_explicit": column_property(tracks_table.c.explicit),
        },
    )

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
