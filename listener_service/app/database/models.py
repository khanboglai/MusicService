from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Table,
    Text,
    ForeignKey,
    BigInteger
)
from sqlalchemy.orm import column_property, registry, relationship, composite

from domain.entities.real.listener import Listener
from domain.events.real.interaction import NewInteractionRegistered
from domain.events.real.like import NewLikeRegistered
from database.connect import engine, Base
from domain.values.real.age import Age
from domain.values.real.name import Name

mapper_registry = registry()


listener_table = Table(
    "User",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger),
    Column("first_name", Text),
    Column("last_name", Text),
    Column("birth_date", Date),
    Column("subscription", Boolean)
)

like_table = Table(
    "TrackLikes",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, ForeignKey("User.id"), nullable=False),
    Column("track_id", BigInteger, nullable=False)
)

interaction_table = Table(
    "Interactions",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, ForeignKey("User.id"), nullable=False),
    Column("track_id", BigInteger, nullable=False),
    Column("last_interaction", DateTime),
    Column("count_interaction", BigInteger),
    Column("listen_time", BigInteger)
)

listener_table.tometadata(Base.metadata)
like_table.tometadata(Base.metadata)
interaction_table.tometadata(Base.metadata)

async def start_mapping():
    mapper_registry.map_imperatively(
        Listener,
        listener_table,
        properties={
            "oid": column_property(listener_table.c.id),
            "user_id": column_property(listener_table.c.user_id),
            "firstname": composite(lambda value: Name(value, True), listener_table.c.first_name),
            "lastname": composite(lambda value: Name(value, True), listener_table.c.last_name),
            "birthdate": composite(lambda value: Age(value, True), listener_table.c.birth_date),
            "subscription": column_property(listener_table.c.subscription),
            "likes": relationship(NewLikeRegistered, back_populates="user", cascade="all, delete-orphan"),
            "interactions": relationship(NewInteractionRegistered, back_populates="user", cascade="all, delete-orphan"),
        },
    )

    mapper_registry.map_imperatively(
        NewLikeRegistered,
        like_table,
        properties={
            "event_id": column_property(like_table.c.id),
            "user": relationship(Listener, back_populates="likes"),
            "track_id": column_property(like_table.c.track_id), 
        },
    )

    mapper_registry.map_imperatively(
        NewInteractionRegistered,
        interaction_table,
        properties={
            "event_id": column_property(interaction_table.c.id),
            "user": relationship(Listener, back_populates="interactions"),
            "track_id": column_property(interaction_table.c.track_id),
            "last_interaction": column_property(interaction_table.c.last_interaction),
            "count_interaction": column_property(interaction_table.c.count_interaction),
            "listen_time": column_property(interaction_table.c.listen_time),
        }
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
