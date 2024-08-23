from logging import getLogger
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from webapp.crud.base import Repository
from webapp.models.bet_maker.bet import Bet, BetStatusEnum
from webapp.models.bet_maker.event import Event
from webapp.schema.bet import BetCreate

logger = getLogger('bet_repository')


class BetRepository(Repository):
    async def get_bet_by_id(self, bet_id: int) -> Bet | None:
        return (await self.session.scalars(select(Bet).where(Bet.id == bet_id))).one_or_none()

    async def update_bets_status(self, bets: Sequence[Bet], status: BetStatusEnum) -> None:
        for bet in bets:
            bet.status = status

        try:
            await self.session.commit()
        except IntegrityError as err:
            logger.error(str(err))

        return None

    async def get_bets_by_event_id(self, event_id: int) -> Sequence[Bet] | None:
        bets = (
            await self.session.scalars(select(Bet).where(Bet.event_id == event_id, Bet.status == BetStatusEnum.WAITING))
        ).all()
        if not bets:
            return None

        return bets

    async def get_all_bets(self) -> Sequence[Bet] | None:
        bets = (await self.session.scalars(select(Bet))).all()
        if not bets:
            return None

        return bets

    async def create_bet(self, event: Event, bet_data: BetCreate) -> Bet | None:
        new_bet = Bet(event_id=event.id, odds=event.odds, amount=bet_data.amount)
        self.session.add(new_bet)

        try:
            await self.session.commit()
        except IntegrityError as err:
            await self.session.rollback()
            logger.error(str(err))
            return None

        return new_bet
