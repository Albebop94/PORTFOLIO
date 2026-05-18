from uuid import uuid4

import pytest
import pytest_asyncio

from src.config import settings
from src.domain.entities import User
from src.infrastructure.database import session as db_session
from src.infrastructure.database.session import Base, init_db
from src.infrastructure.repositories.user_repository import SqlAlchemyUserRepository


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    init_db(settings.database_url)
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await db_session.engine.dispose()


@pytest_asyncio.fixture
async def session():
    factory = db_session.get_session_factory()
    async with factory() as s:
        yield s


@pytest_asyncio.fixture
def repo(session):
    return SqlAlchemyUserRepository(session)


@pytest.mark.asyncio
async def test_add_and_get_user(repo, session):
    user_id = uuid4()
    user = User(username="repo_user", email="repo@example.com", id=user_id)

    await repo.add(user)
    await session.commit()

    # Test get_by_id
    saved_user = await repo.get_by_id(user_id)
    assert saved_user is not None
    assert saved_user.id == user_id
    assert saved_user.username == "repo_user"
    assert saved_user.email == "repo@example.com"

    # Test get_by_email
    saved_user_by_email = await repo.get_by_email("repo@example.com")
    assert saved_user_by_email is not None
    assert saved_user_by_email.id == user_id


@pytest.mark.asyncio
async def test_get_non_existent_user(repo):
    user = await repo.get_by_id(uuid4())
    assert user is None

    user_by_email = await repo.get_by_email("nonexistent@example.com")
    assert user_by_email is None
