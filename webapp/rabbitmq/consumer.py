import asyncio
from logging import getLogger

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, ExchangeType
from aiormq import AMQPException
from orjson import JSONDecodeError, loads
from pydantic import ValidationError

from conf.config import settings
from webapp.rabbitmq.handlers.event import handle_event_from_provider
from webapp.schema.event import EventFromProvider
from webapp.schema.rabbitmq.message import BaseMessage

TIMEOUT_ON_ERROR = 10

logger = getLogger('consumer')


async def start_consuming() -> None:
    while True:
        try:
            connection = await connect_robust(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                login=settings.RABBITMQ_USER,
                password=settings.RABBITMQ_PASSWORD,
            )
            channel = await connection.channel(publisher_confirms=False)

            await channel.set_qos(prefetch_count=settings.RABBITMQ_MAX_MESSAGE_COUNT)

            exchange = await channel.declare_exchange(settings.RABBITMQ_PROVIDER_EXCHANGE_NAME, ExchangeType.FANOUT)

            queue = await channel.declare_queue(settings.RABBITMQ_PROVIDER_QUEUE_NAME)
            await queue.bind(exchange)

            await queue.consume(process_message)

            logger.info('Subscription succeed')

            await asyncio.Future()

        except AMQPException as err:
            logger.error(str(err))
            await asyncio.sleep(TIMEOUT_ON_ERROR)


async def process_message(message: AbstractIncomingMessage) -> None:
    try:
        data = loads(message.body)
    except JSONDecodeError as err:
        logger.error(str(err))
        return

    logger.info('Message received')

    try:
        validated_data = BaseMessage(**data)
    except ValidationError as err:
        logger.error(str(err))
        await message.channel.basic_ack(message.delivery_tag)
        return

    await handle_message(validated_data)
    await message.channel.basic_ack(message.delivery_tag)


async def handle_message(message: BaseMessage) -> None:
    try:
        event = EventFromProvider(**message.message)
    except ValidationError as err:
        logger.error(str(err))
        return

    await handle_event_from_provider(event)
