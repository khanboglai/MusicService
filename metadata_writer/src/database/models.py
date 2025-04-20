from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    ForeignKey,
    )

from src.database.postgres import Base

class AlbumMetadata(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    aitist_id = Column(Integer)
    title = Column(String)
    release_date = Column(Date)

    track = relationship("TrackMetadata", back_populates="albums", uselist=False, cascade="all, delete-orphan")


class TrackMetadata(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"))
    title = Column(String)

    album = relationship("AlbumMetadata", back_populates="tracks")