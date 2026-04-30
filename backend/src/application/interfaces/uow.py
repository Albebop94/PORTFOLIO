from abc import ABC, abstractmethod
from typing import Any

from src.application.interfaces.repository import UserRepository


class UnitOfWork(ABC):
    users: UserRepository

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
