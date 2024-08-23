import json
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, List

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from webapp.db.postgres import engine, get_session
from webapp.models.meta import metadata


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test.com") as client:
        yield client


@pytest.fixture()
async def db_session(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as connection:
        session_maker = async_sessionmaker(bind=connection, expire_on_commit=False)
        session = session_maker()

        async def mocked_session() -> AsyncGenerator[AsyncSession, None]:
            yield session

        app.dependency_overrides[get_session] = mocked_session  # noqa

        yield session

        await connection.rollback()


@pytest.fixture()
async def _load_fixtures(db_session: AsyncSession, fixtures: List[Path]) -> None:
    for fixture in fixtures:
        fixture_path = Path(fixture)
        model = metadata.tables[fixture_path.stem]

        with open(fixture_path, "r") as file:
            values = json.load(file)

        for model_obj in values:
            for key, value in model_obj.items():
                if "deadline" in key:
                    model_obj[key] = datetime.fromisoformat(value)

        await db_session.execute(insert(model).values(values))
        await db_session.commit()

    return


@pytest.fixture()
async def _common_api_fixture(
    _load_fixtures: None,
) -> None:
    return
