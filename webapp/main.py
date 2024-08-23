from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncIterator

from aiormq import AMQPException
from fastapi import FastAPI

from webapp.api.router import router
from webapp.on_startup.logger import setup_logger
from webapp.rabbitmq.consumer import start_consuming

logger = getLogger(__name__)


def setup_routers(app: FastAPI) -> None:
    app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logger()

    try:
        await start_consuming()
    except AMQPException as err:
        logger.error(err)

    logger.info('START APP')
    yield
    logger.info('END APP')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_routers(app)

    return app
