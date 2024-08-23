from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from webapp.api.event.router import event_router
from webapp.crud.event import EventRepository
from webapp.db.postgres import get_session
from webapp.schema.event import ActualEventResponse


@event_router.get('/events', response_model=ActualEventResponse)
async def get_events_handler(
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    event_repo = EventRepository(session)

    events = await event_repo.get_actual_events()
    if events is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Events not found')

    return ORJSONResponse(
        content=ActualEventResponse(count=len(events), result=events).model_dump(mode='json'), status_code=HTTP_200_OK
    )
