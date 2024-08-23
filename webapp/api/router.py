from fastapi import APIRouter

from webapp.api.bet.router import bet_router
from webapp.api.event.router import event_router

router = APIRouter()

router.include_router(event_router, tags=['Event'])
router.include_router(bet_router, tags=['Bet'])
