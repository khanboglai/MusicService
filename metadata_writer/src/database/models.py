from sqlalchemy import Column, Date, BigInteger, Table, Text, Boolean
from sqlalchemy.orm import column_property, registry
from src.entities.album import Album
from src.entities.track import Track

mapper_registry = registry()

albums_table = Table(
    "albums",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("title", Text),
    Column("release_date", Date(timezone=True)),
)

tracks_table = Table(
    "tracks",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("album_id", BigInteger),
    Column("title", Text),
    Column("explicit", Boolean),
)


def start_mapping():
    mapper_registry.map_imperatively(
        Album,
        albums_table,
        properties={
            "__id": column_property(albums_table.c.id),
            "__title": column_property(albums_table.c.title),
            "__release_date": column_property(albums_table.c.release_date),
        },
    )

    mapper_registry.map_imperatively(
        Track,
        tracks_table,
        properties={
            "__id": column_property(tracks_table.c.id),
            "__album_id": column_property(tracks_table.c.album_id),
            "__title": column_property(tracks_table.c.title),
            "__explicit": column_property(tracks_table.c.explicit),
        },
    )