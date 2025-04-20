from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    ForeignKey,
    ARRAY,
    Float,
    DateTime
    )

from src.database.postgres import Base

class AlbumMetadata(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)


class TrackMetadata(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    title = Column(String)