from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.uow import UnitOfWork
from src.infrastructure.repositories.user_repository import SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = SqlAlchemyUserRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
