import asyncio
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession

from webapp.crud.bet import BetRepository
from webapp.crud.event import EventRepository
from webapp.db.postgres import get_session
from webapp.models.bet_maker.bet import BetStatusEnum
from webapp.models.bet_maker.event import Event, EventStatusEnum
from webapp.schema.event import EventFromProvider

logger = getLogger('event_handler')


async def handle_event_from_provider(message: EventFromProvider) -> None:
    async for session in get_session():
        event_repo = EventRepository(session)
        event, is_created = await event_repo.create_or_update_from_provider(message)

        if event is None:
            logger.error({'event': 'Got bad message', 'data': message})
            return

        if event.status != EventStatusEnum.WAITING.value and not is_created:
            await asyncio.create_task(process_bets(session, event))

        logger.info({'event': 'Processed event message', 'is_created': is_created})


async def process_bets(session: AsyncSession, event: Event) -> None:
    bet_repo = BetRepository(session)
    bets = await bet_repo.get_bets_by_event_id(event.id)
    if bets is not None:
        await bet_repo.update_bets_status(bets, event_status_to_bet_status[event.status])


event_status_to_bet_status: dict[EventStatusEnum, BetStatusEnum] = {
    EventStatusEnum.W1: BetStatusEnum.WON,
    EventStatusEnum.W2: BetStatusEnum.LOST,
}
