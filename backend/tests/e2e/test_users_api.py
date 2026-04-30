import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.infrastructure.database import session as db_session
from src.infrastructure.database.session import Base, init_db
from src.main import app


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    init_db(settings.database_url)
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db_session.engine.dispose()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_and_get_user(client: AsyncClient):
    # Test Create
    response = await client.post(
        "/api/v1/users/", json={"username": "testuser", "email": "test@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

    user_id = data["id"]

    # Test Get
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser"

    # Test Duplicate
    response = await client.post(
        "/api/v1/users/", json={"username": "anotheruser", "email": "test@example.com"}
    )
    assert response.status_code == 400

    # Test Not Found
    import uuid
    random_id = uuid.uuid4()
    response = await client.get(f"/api/v1/users/{random_id}")
    assert response.status_code == 404
