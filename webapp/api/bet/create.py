from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from webapp.api.bet.router import bet_router
from webapp.crud.bet import BetRepository
from webapp.crud.event import EventRepository
from webapp.db.postgres import get_session
from webapp.schema.bet import BetCreate, BetResponse


@bet_router.post('/bet', response_model=BetResponse, status_code=HTTP_201_CREATED)
async def create_bet_handler(
    body: BetCreate,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    event = await EventRepository(session).get_actual_event_by_id(body.event_id)
    if event is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Event not found or not relevant')

    created_bet = await BetRepository(session).create_bet(event, body)
    if created_bet is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    return ORJSONResponse(
        content=BetResponse.model_validate(created_bet).model_dump(mode='json'), status_code=HTTP_201_CREATED
    )
