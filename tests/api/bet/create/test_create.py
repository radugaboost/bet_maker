from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("body", "expected_status", "fixtures"),
    [
        (
            {"event_id": "0", "amount": 12000},
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / "bet_maker.event.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_create_bet(
    client: AsyncClient,
    body: Dict[str, Any],
    expected_status: int,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS["bet"]["create"],
        json=body,
    )

    assert response.status_code == expected_status
