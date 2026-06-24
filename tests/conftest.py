import copy
import pytest
from pytest_asyncio import fixture as async_fixture
from httpx import AsyncClient, ASGITransport
import src.app as app_module

# Take a deep copy of the initial activities at import time
ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities before each test."""
    app_module.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)

@async_fixture
async def client():
    """Async HTTP client for testing the FastAPI app."""
    transport = ASGITransport(app=app_module.app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
