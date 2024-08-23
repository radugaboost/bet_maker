from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("bet_id", "expected_status", "fixtures"),
    [
        (
            "0",
            status.HTTP_200_OK,
            [FIXTURES_PATH / "bet_maker.event.json", FIXTURES_PATH / "bet_maker.bet.json"],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_bet(
    client: AsyncClient,
    bet_id: str,
    expected_status: int,
) -> None:
    response = await client.get(
        "".join([URLS["bet"]["info"], bet_id]),
    )
    assert response.status_code == expected_status
