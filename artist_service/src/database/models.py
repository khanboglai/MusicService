""" тут таблицы и маппинг """


from sqlalchemy import Column, DateTime, Integer, String, Table, Text
from sqlalchemy.orm import column_property, registry, composite
from src.models.artist import Artist
from src.value_objects.artist_description import Description
from src.database.postgres import engine

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


async def start_mapping():
    mapper_registry.map_imperatively(
        Artist,
        artist_table,
        properties={
            "__id": column_property(artist_table.c.id),
            "__name": column_property(artist_table.c.name),
            "__registered_at": column_property(artist_table.c.registered_at),
            "__cover_path": column_property(artist_table.c.cover_path),
            "__description": composite(lambda value: Description(value), artist_table.c.description),
        },
    )

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
