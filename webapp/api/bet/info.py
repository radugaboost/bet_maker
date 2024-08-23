from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from webapp.api.bet.router import bet_router
from webapp.crud.bet import BetRepository
from webapp.db.postgres import get_session
from webapp.schema.bet import BetResponse, ListBetResponse


@bet_router.get('/bet/{bet_id}', response_model=BetResponse)
async def get_bet_info_handler(bet_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    bet = await BetRepository(session).get_bet_by_id(bet_id)
    if bet is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Bet not found')

    return ORJSONResponse(content=BetResponse.model_validate(bet).model_dump(mode='json'), status_code=HTTP_200_OK)


@bet_router.get('/bets', response_model=ListBetResponse)
async def get_list_bet_info_handler(
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    bets = await BetRepository(session).get_all_bets()
    if bets is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Bets not found')

    return ORJSONResponse(
        content=ListBetResponse(count=len(bets), result=bets).model_dump(mode='json'), status_code=HTTP_200_OK
    )
