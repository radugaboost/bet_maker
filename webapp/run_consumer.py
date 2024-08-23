import asyncio
from logging import getLogger

from webapp.on_startup.logger import setup_logger
from webapp.rabbitmq.consumer import start_consuming

TIMEOUT_ON_ERROR = 10

logger = getLogger(__name__)

if __name__ == '__main__':
    print('Starting consuming')

    setup_logger()

    asyncio.run(start_consuming())
