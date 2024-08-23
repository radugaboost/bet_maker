from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.bet_maker.base import BaseModel
from webapp.models.meta import DEFAULT_SCHEMA

if TYPE_CHECKING:
    from webapp.models.bet_maker.event import Event


class BetStatusEnum(Enum):
    WAITING: str = 'waiting'
    WON: str = 'won'
    LOST: str = 'lost'


class Bet(BaseModel):
    __tablename__ = 'bet'

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f'{DEFAULT_SCHEMA}.event.id', ondelete='CASCADE'), nullable=False
    )
    event: Mapped['Event'] = relationship('Event', back_populates='bets')

    status: Mapped[BetStatusEnum] = mapped_column(
        ENUM(BetStatusEnum, inherit_schema=True), default=BetStatusEnum.WAITING
    )
    amount: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    odds: Mapped[Decimal] = mapped_column(Numeric(100, 2), nullable=False)
