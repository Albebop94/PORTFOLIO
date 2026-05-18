import pytest
import pytest_asyncio
from sqlalchemy import text

from src.config import settings
from src.domain.entities import User
from src.infrastructure.database import session as db_session
from src.infrastructure.database.session import Base, init_db
from src.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork


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
def session_factory():
    return db_session.get_session_factory()


@pytest.mark.asyncio
async def test_uow_commit(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)

    async with uow:
        user = User(username="uow_commit_user", email="uow_commit@example.com")
        await uow.users.add(user)
        await uow.commit()

    # Verify data is committed using a new session
    async with session_factory() as session:
        result = await session.execute(
            text("SELECT username FROM users WHERE email='uow_commit@example.com'")
        )
        row = result.fetchone()
        assert row is not None
        assert row[0] == "uow_commit_user"


@pytest.mark.asyncio
async def test_uow_rollback(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)

    try:
        async with uow:
            user = User(username="uow_rollback_user", email="uow_rollback@example.com")
            await uow.users.add(user)
            # Simulate an exception
            raise RuntimeError("Something went wrong")
    except RuntimeError:
        pass

    # Verify data is NOT committed
    async with session_factory() as session:
        result = await session.execute(
            text("SELECT username FROM users WHERE email='uow_rollback@example.com'")
        )
        row = result.fetchone()
        assert row is None
