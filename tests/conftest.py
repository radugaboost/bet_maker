import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI

from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig

from conf.config import settings
from webapp.main import create_app


@pytest.fixture(scope="session")
async def app(_migrate_db: None) -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def alembic_config() -> AlembicConfig:
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.db_url)

    return alembic_cfg


@pytest.fixture(scope="session")
async def _migrate_db(alembic_config: AlembicConfig) -> AsyncGenerator[None, None]:
    upgrade(alembic_config, "head")
    yield
    downgrade(alembic_config, "base")
