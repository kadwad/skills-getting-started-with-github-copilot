import pytest
from urllib.parse import quote
import src.app as app_module

@pytest.mark.asyncio
async def test_get_activities(client):
    # Arrange
    # app state is provided by fixtures

    # Act
    resp = await client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "async@test"
    url_activity = quote(activity)

    # Act
    resp = await client.post(f"/activities/{url_activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

@pytest.mark.asyncio
async def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "async@test"
    url_activity = quote(activity)

    # Act
    resp1 = await client.post(f"/activities/{url_activity}/signup", params={"email": email})
    resp2 = await client.post(f"/activities/{url_activity}/signup", params={"email": email})

    # Assert
    assert resp1.status_code == 200
    assert resp2.status_code == 400

@pytest.mark.asyncio
async def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "async@test"
    url_activity = quote(activity)
    await client.post(f"/activities/{url_activity}/signup", params={"email": email})

    # Act
    resp = await client.delete(f"/activities/{url_activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]

@pytest.mark.asyncio
async def test_unregister_nonexistent_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "nonexistent@test"
    url_activity = quote(activity)

    # Act
    resp = await client.delete(f"/activities/{url_activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
