from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.repository.abc.listener import BaseListenerRepo
from infra.database.repository.real.listener import ListenerRepository
from dependencies.registrator import add_factory_to_mapper
from domain.entities.real.listener import Listener
from infra.database.connect import get_session


@add_factory_to_mapper(BaseListenerRepo)
def create_listener_repo(session: AsyncSession = Depends(get_session)) -> BaseListenerRepo:
    return ListenerRepository(session)
