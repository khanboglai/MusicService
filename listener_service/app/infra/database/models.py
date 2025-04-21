from uuid import UUID, uuid4
from sqlalchemy import (
    UUID,
    Integer,
    Boolean,
    Column,
    Date,
    Time,
    Table,
    Text,
    ForeignKey
)
from sqlalchemy.orm import column_property, registry, relationship

from domain.entities.real.listener import Listener
from domain.events.real.interaction import NewInteractionRegistered
from domain.events.real.like import NewLikeRegistered

mapper_registry = registry()


listener_table = Table(
    "User",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("first_name", Text),
    Column("last_name", Text),
    Column("birth_date", Date),
    Column("subscription", Boolean)
)

like_table = Table(
    "TrackLikes",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("User.id"), nullable=False),
    Column("track_id", UUID(as_uuid=True), nullable=False)
)

interaction_table = Table(
    "Interactions",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("User.id"), nullable=False),
    Column("track_id", UUID(as_uuid=True), nullable=False),
    Column("last_interactions", Time),
    Column("count_interaction", Integer),
    Column("listen_time", Time)
)

def start_mapping():
    mapper_registry.map_imperatively(
        Listener,
        listener_table,
        properties={
            "oid": column_property(listener_table.c.id),
            "first_name": column_property(listener_table.c.first_name),
            "last_name": column_property(listener_table.c.last_name),
            "birth_date": column_property(listener_table.c.birth_date),
            "subscription": column_property(listener_table.c.subscription),
            "likes": relationship("TrackLikes", back_populates="user_id"),
            "interactions": relationship("Interactions", back_populates="user_id"),
        },
    )

    mapper_registry.map_imperatively(
        NewLikeRegistered,
        like_table,
        properties={
            "event_id": column_property(like_table.c.id),
            "user_id": relationship("User", back_populates="likes"),
            "track_id": column_property(like_table.c.track_id), 
        },
    )

    mapper_registry.map_imperatively(
        NewInteractionRegistered,
        interaction_table,
        properties={
            "event_id": column_property(interaction_table.c.id),
            "user_id": relationship("User", back_populates="interactions"),
            "track_id": column_property(interaction_table.c.track_id),
            "last_interaction": column_property(interaction_table.c.last_interaction),
            "count_interaction": column_property(interaction_table.c.count_interaction),
            "listen_time": column_property(interaction_table.c.listen_time),
        }
    )
