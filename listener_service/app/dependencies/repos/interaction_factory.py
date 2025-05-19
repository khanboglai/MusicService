from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.repository.abc.interaction import BaseInteractionRepo
from database.repository.real.interaction import InteractionRepository
from dependencies.registrator import add_factory_to_mapper
from database.connect import get_session


@add_factory_to_mapper(BaseInteractionRepo)
def create_interaction_repo(session: AsyncSession = Depends(get_session)) -> BaseInteractionRepo:
    return InteractionRepository(session)