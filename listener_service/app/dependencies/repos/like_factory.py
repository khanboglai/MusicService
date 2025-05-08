from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.repository.abc.like import BaseLikeRepo
from database.repository.real.like import LikeRepository
from dependencies.registrator import add_factory_to_mapper
from database.connect import get_session


@add_factory_to_mapper(BaseLikeRepo)
def create_like_repo(session: AsyncSession = Depends(get_session)) -> BaseLikeRepo:
    return LikeRepository(session)
