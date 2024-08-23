from datetime import datetime
from logging import getLogger
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from webapp.crud.base import Repository
from webapp.models.bet_maker.event import Event, EventStatusEnum
from webapp.schema.event import EventFromProvider

logger = getLogger('event_repository')


class EventRepository(Repository):
    async def get_event_by_id(self, event_id: int) -> Event | None:
        return await self.session.get(Event, event_id)

    async def get_actual_event_by_id(self, event_id: int) -> Event | None:
        query = select(Event).where(
            Event.deadline > datetime.utcnow(), Event.id == event_id, Event.status == EventStatusEnum.WAITING
        )
        return (await self.session.scalars(query)).one_or_none()

    async def get_actual_events(self) -> Sequence[Event] | None:
        query = select(Event).where(Event.deadline > datetime.utcnow(), Event.status == EventStatusEnum.WAITING)

        result = (await self.session.scalars(query)).all()
        if not result:
            return None

        return result

    async def create_event_from_provider(self, event_data: EventFromProvider) -> Event | None:
        new_event = Event(**event_data.model_dump())
        self.session.add(new_event)

        try:
            await self.session.commit()
        except IntegrityError as err:
            await self.session.rollback()
            logger.error(str(err))
            return None

        return new_event

    async def update_event_from_provider(self, event: Event, event_data: EventFromProvider) -> Event | None:
        for key, value in event_data.model_dump(exclude_unset=True).items():
            setattr(event, key, value)

        try:
            await self.session.commit()
        except IntegrityError as err:
            await self.session.rollback()
            logger.error(str(err))
            return None

        await self.session.refresh(event)

        return event

    async def create_or_update_from_provider(
        self, event_data: EventFromProvider
    ) -> tuple[Event, bool] | tuple[None, bool]:
        event = await self.get_event_by_id(event_data.id)
        if event is None:
            created_event = await self.create_event_from_provider(event_data)
            if created_event is None:
                return None, False

            return created_event, True

        updated_event = await self.update_event_from_provider(event, event_data)
        if updated_event is None:
            return None, False

        return updated_event, False
