from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from database.repository.abc.like import BaseLikeRepo
from domain.events.real.like import NewLikeRegistered
from database.exceptions.real.unique import UniqueException
from database.exceptions.real.existance import NotExistException
from domain.entities.real.listener import Listener


class LikeRepository(BaseLikeRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_like(self, *, like: NewLikeRegistered) -> NewLikeRegistered:
        statement = (
            select(NewLikeRegistered)
            .where(
                (NewLikeRegistered.user == like.user) &
                (NewLikeRegistered.track_id == like.track_id)
            )
        )
        result = await self.session.execute(statement=statement)
        if result.scalar_one_or_none():
            raise UniqueException()
        
        self.session.add(like)
        await self.session.commit()
        return like
    
    async def delete_like(self, *, listener: Listener, track_id: int):
        statement = (
            select(NewLikeRegistered)
            .where(
                (NewLikeRegistered.user == listener) &
                (NewLikeRegistered.track_id == track_id)
            )
        )
        result = await self.session.execute(statement=statement)
        result = result.scalar_one_or_none()
        if not result:
            raise NotExistException()
        
        await self.session.delete(result)
        await self.session.commit()
