from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime

from domain.events.real.interaction import NewInteractionRegistered
from database.repository.abc.interaction import BaseInteractionRepo
from domain.entities.real.listener import Listener
from database.exceptions.real.existance import NotExistException
from database.exceptions.abc.base import DatabaseException


class InteractionRepository(BaseInteractionRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_interaction_by_ids(self, *, listener: Listener, track_id: int) -> NewInteractionRegistered:
        statement = (
            select(NewInteractionRegistered)
            .where(
                (NewInteractionRegistered.user == listener) &
                (NewInteractionRegistered.track_id == track_id)
            )
        )
        result = await self.session.execute(statement=statement)
        result = result.scalar_one_or_none()
        if not result:
            raise NotExistException()
        return result

    async def add_or_update_interaction(self, *, listener: Listener, track_id: int, listen_time: int) -> NewInteractionRegistered:
        try:
            old_interaction = await self.get_interaction_by_ids(listener=listener, track_id=track_id)
            statement = (
                update(NewInteractionRegistered)
                .where(
                    NewInteractionRegistered.event_id == old_interaction.event_id
                )
                .values(
                    last_interaction=datetime.now(),
                    count_interaction=(old_interaction.count_interaction + 1),
                    listen_time=listen_time,
                )
            )
            await self.session.execute(statement=statement)
            await self.session.commit()
            new_interaction = await self.get_interaction_by_ids(listener=listener, track_id=track_id)
            return new_interaction
        except DatabaseException:
            interaction = NewInteractionRegistered(listener_id=listener, track_id=track_id, listen_time=listen_time)
            self.session.add(interaction)
            await self.session.commit()
            return interaction
        