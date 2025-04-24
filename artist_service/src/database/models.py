""" тут таблицы и маппинг """


from sqlalchemy import Column, DateTime, Integer, String, Table, Text
from sqlalchemy.orm import column_property, registry
from src.models.artist import Artist


mapper_registry = registry()


artist_table = Table(
    "artists",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", Text),
    Column("registered_at", DateTime(timezone=True)),
    Column("cover_path", Text),
    Column("description", Text),
)


def start_mapping():
    mapper_registry.map_imperatively(
        Artist,
        artist_table,
        properties={
            "__id": column_property(artist_table.c.id),
            "__name": column_property(artist_table.c.name),
            "__registered_at": column_property(artist_table.c.registered_at),
            "__cover_path": column_property(artist_table.c.cover_path),
            "__description": column_property(artist_table.c.description),
        },
    )
