""" тут таблицы и маппинг """


from sqlalchemy import Column, DateTime, Integer, String, Table, Text
from sqlalchemy.orm import column_property, registry, composite
from src.models.artist import Artist
from src.models.custom_types.description import DescriptionType
from src.database.postgres import engine, Base


mapper_registry = registry()


artist_table = Table(
    "artists",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", Text, unique=True, nullable=False),
    Column("email", Text, unique=True),
    Column("registered_at", DateTime(timezone=True)),
    Column("description", DescriptionType),
    Column("user_id", Integer, unique=True, nullable=False),
)

artist_table.tometadata(Base.metadata) # регистрация таблицы для миграции

async def start_mapping():
    mapper_registry.map_imperatively(
        Artist,
        artist_table,
        properties={
            "oid": column_property(artist_table.c.id),
            "_name": column_property(artist_table.c.name),
            "_email": column_property(artist_table.c.email),
            "_registered_at": column_property(artist_table.c.registered_at),
            "_description": column_property(artist_table.c.description),
            "_user_id": column_property(artist_table.c.user_id),
            # composite для маппинга нескольких столбцов, он нам не подойдет в данном случае
        },
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
