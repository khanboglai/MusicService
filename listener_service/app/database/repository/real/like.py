""" Определение слоя репозиториев для лайков """
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.repository.abc.like import BaseLikeRepo
from domain.events.real.like import NewLikeRegistered
from database.exceptions.real.unique import UniqueException
from database.exceptions.real.existance import NotExistException
from database.exceptions.abc.base import DatabaseException
from domain.entities.real.listener import Listener


class LikeRepository(BaseLikeRepo):
    """ Слой репозиториев для лайков """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_like_by_ids(self, *, listener: Listener, track_id: int) -> NewLikeRegistered:
        """ Получение лайка по слушателю и track_id """
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
            raise NotExistException
        return result

    async def add_or_delete_like(self, *, listener: Listener, track_id: int) -> NewLikeRegistered:
        """ Добавление или удаление лайка на трек с track_id """
        try:
            like = await self.get_like_by_ids(listener=listener, track_id=track_id)
            await self.session.delete(like)
            await self.session.commit()
        except NotExistException:
            like = NewLikeRegistered(user_id=listener, track_id=track_id)
            self.session.add(like)
            await self.session.commit()
            return like
            