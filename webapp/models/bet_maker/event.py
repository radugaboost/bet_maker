from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from conf.config import settings
from webapp.models.bet_maker.base import BaseModel

if TYPE_CHECKING:
    from webapp.models.bet_maker.bet import Bet


class EventStatusEnum(Enum):
    WAITING: str = 'waiting'
    W1: str = 'W1'
    W2: str = 'W2'


class Event(BaseModel):
    __tablename__ = 'event'

    name: Mapped[str] = mapped_column(String(settings.NAME_MAX_LENGTH), nullable=False)
    status: Mapped[EventStatusEnum] = mapped_column(
        ENUM(EventStatusEnum, inherit_schema=True), default=EventStatusEnum.WAITING
    )
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    odds: Mapped[Decimal] = mapped_column(Numeric(100, 2), nullable=False)

    bets: Mapped[list['Bet']] = relationship('Bet', back_populates='event')
