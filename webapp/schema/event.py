from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, model_validator

from webapp.models.bet_maker.event import EventStatusEnum


class EventResponse(BaseModel):
    id: int
    name: str
    status: EventStatusEnum
    deadline: datetime
    odds: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used='json'),
    ]

    model_config = ConfigDict(from_attributes=True)


class ActualEventResponse(BaseModel):
    count: int
    result: list[EventResponse]


class EventFromProvider(BaseModel):
    id: int
    name: str
    status: EventStatusEnum
    deadline: datetime
    odds: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used='json'),
    ] = Field(..., gt=1)
    created_at: datetime
    updated_at: datetime

    @model_validator(mode='after')
    def validate_odds(self) -> "EventFromProvider":
        if len(str(self.odds).rsplit('.')[-1]) != 2:
            raise ValueError('Invalid odds format. Must be 2 decimal places')

        return self
