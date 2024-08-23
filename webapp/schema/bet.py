from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from webapp.models.bet_maker.bet import BetStatusEnum


class BetCreate(BaseModel):
    event_id: int
    amount: Decimal = Field(..., gt=0)


class BetResponse(BaseModel):
    id: int
    event_id: int
    status: BetStatusEnum
    amount: Decimal
    odds: Decimal

    @field_serializer('amount', 'odds', when_used='json')
    def serialize_decimal(self, v: Decimal) -> float:
        return float(v)

    model_config = ConfigDict(from_attributes=True)


class ListBetResponse(BaseModel):
    count: int
    result: list[BetResponse]
