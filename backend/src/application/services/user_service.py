from uuid import UUID

from src.application.interfaces.uow import UnitOfWork
from src.domain.entities import User
from src.domain.exceptions import UserAlreadyExistsError, UserNotFoundError


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, username: str, email: str) -> User:
        async with self.uow:
            existing_user = await self.uow.users.get_by_email(email)
            if existing_user:
                raise UserAlreadyExistsError(email)

            user = User(username=username, email=email)
            await self.uow.users.add(user)
            await self.uow.commit()
            return user

    async def get_user(self, user_id: UUID) -> User:
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(str(user_id))
            return user
