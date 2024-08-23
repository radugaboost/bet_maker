from datetime import timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_HOST: str
    BIND_PORT: int

    PG_DBNAME: str
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_PROVIDER_QUEUE_NAME: str
    RABBITMQ_PROVIDER_EXCHANGE_NAME: str
    RABBITMQ_MAX_MESSAGE_COUNT: int

    LOG_LEVEL: str = 'debug'

    FILE_EXPIRE_TIME: timedelta = timedelta(minutes=15)

    NAME_MAX_LENGTH: int = 128

    @property
    def db_url(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DBNAME}'


settings = Settings()
