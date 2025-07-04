""" Маппинг моделей в таблицы в бд """
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
from domain.events.real.interaction import NewInteractionRegistered, NewInteractionAnalyticsRegistered
from domain.events.real.like import NewLikeRegistered
from domain.events.real.playlist import NewPlaylistRegistered, PlaylistTrack
from database.connect import engine, Base
from domain.values.real.age import Age
from domain.values.real.name import Name

mapper_registry = registry()


listener_table = Table(
    "User",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, unique=True),
    Column("first_name", Text),
    Column("last_name", Text),
    Column("birth_date", Date),
    Column("subscription", Boolean)
)

like_table = Table(
    "TrackLikes",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, ForeignKey("User.user_id"), nullable=False),
    Column("track_id", BigInteger, nullable=False)
)

interaction_table = Table(
    "Interactions",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, ForeignKey("User.user_id"), nullable=False),
    Column("track_id", BigInteger, nullable=False),
    Column("last_interaction", DateTime),
    # Column("count_interaction", BigInteger),
    Column("listen_time", BigInteger)
)

analytics_interaction_table = Table(
    "AnalyticsInteractions",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, ForeignKey("User.user_id"), nullable=False),
    Column("track_id", BigInteger, nullable=False),
    Column("track_name", Text),
    Column("last_interaction", DateTime),
    # Column("count_interaction", BigInteger),
    Column("listen_time", BigInteger),
    Column("artist_id", BigInteger, nullable=False),
    Column("artist_name", Text),
    Column("genre_id", BigInteger, nullable=False),
    Column("genre_name", Text)
)

playlist_table = Table(
    "Playlists",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, ForeignKey("User.user_id"), nullable=False),
    Column("title", Text, nullable=False),
)

playlist_track_table = Table(
    "PlaylistTracks",
    mapper_registry.metadata,
    Column("playlist_id", BigInteger, ForeignKey("Playlists.id"), primary_key=True),
    Column("track_id", BigInteger, nullable=False, primary_key=True),
)

listener_table.tometadata(Base.metadata)
like_table.tometadata(Base.metadata)
interaction_table.tometadata(Base.metadata)
analytics_interaction_table.tometadata(Base.metadata)
playlist_table.tometadata(Base.metadata)
playlist_track_table.tometadata(Base.metadata)

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
            "analytics_interactions": relationship(NewInteractionAnalyticsRegistered, back_populates="user", cascade="all, delete-orphan"),
            "playlists": relationship(NewPlaylistRegistered, back_populates="user", cascade="all, delete-orphan"),
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
            # "count_interaction": column_property(interaction_table.c.count_interaction),
            "listen_time": column_property(interaction_table.c.listen_time),
        }
    )

    mapper_registry.map_imperatively(
        NewInteractionAnalyticsRegistered,
        analytics_interaction_table,
        properties={
            "event_id": column_property(analytics_interaction_table.c.id),
            "user": relationship(Listener, back_populates="analytics_interactions"),
            "track_id": column_property(analytics_interaction_table.c.track_id),
            "track_name": column_property(analytics_interaction_table.c.track_name),
            "last_interaction": column_property(analytics_interaction_table.c.last_interaction),
            # "count_interaction": column_property(analytics_interaction_table.c.count_interaction),
            "listen_time": column_property(analytics_interaction_table.c.listen_time),
            "artist_id": column_property(analytics_interaction_table.c.artist_id),
            "artist_name": column_property(analytics_interaction_table.c.artist_name),
            "genre_id": column_property(analytics_interaction_table.c.genre_id),
            "genre_name": column_property(analytics_interaction_table.c.genre_name),
        }
    )

    mapper_registry.map_imperatively(
        NewPlaylistRegistered,
        playlist_table,
        properties={
            "event_id": column_property(playlist_table.c.id),
            "user": relationship(Listener, back_populates="playlists"),
            "title": column_property(playlist_table.c.title),
            "tracks": relationship(PlaylistTrack, back_populates="playlist", cascade="all, delete-orphan"),
        },
    )

    mapper_registry.map_imperatively(
        PlaylistTrack,
        playlist_track_table,
        properties={
            "playlist": relationship(NewPlaylistRegistered, back_populates="tracks"),
            "track_id": column_property(playlist_track_table.c.track_id),
        }
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
