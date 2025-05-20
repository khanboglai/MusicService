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
        return result

    async def add_or_update_interaction(self, *, listener: Listener, track_id: int, listen_time: int) -> NewInteractionRegistered:
        interaction = await self.get_interaction_by_ids(listener=listener, track_id=track_id)
        if interaction:
            interaction.last_interaction = datetime.now()
            interaction.count_interaction += 1
            interaction.listen_time = listen_time
        else:
            interaction = NewInteractionRegistered(user_id=listener, track_id=track_id, listen_time=listen_time)
            self.session.add(interaction)

        await self.session.commit()
        await self.session.refresh(interaction, ["user"])
        return interaction        
        