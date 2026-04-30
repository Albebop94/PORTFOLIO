from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.interfaces.repository import UserRepository
from src.application.interfaces.uow import UnitOfWork
from src.application.services.user_service import UserService
from src.domain.entities import User
from src.domain.exceptions import UserAlreadyExistsError, UserNotFoundError


class MockUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    async def get_by_id(self, user_id):
        return self.users.get(user_id)

    async def get_by_email(self, email):
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    async def add(self, user):
        self.users[user.id] = user


class MockUnitOfWork(UnitOfWork):
    def __init__(self):
        self.users = MockUserRepository()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True


@pytest.fixture
def uow():
    return MockUnitOfWork()


@pytest.fixture
def user_service(uow):
    return UserService(uow)


@pytest.mark.asyncio
async def test_create_user_success(user_service, uow):
    user = await user_service.create_user(username="testuser", email="test@example.com")
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    
    # Verify UoW commit was called
    assert uow.committed is True
    
    # Verify user was added to repository
    saved_user = await uow.users.get_by_id(user.id)
    assert saved_user is not None
    assert saved_user.email == "test@example.com"


@pytest.mark.asyncio
async def test_create_user_already_exists(user_service, uow):
    # Setup existing user
    existing_user = User(username="existing", email="test@example.com")
    await uow.users.add(existing_user)
    
    with pytest.raises(UserAlreadyExistsError):
        await user_service.create_user(username="newuser", email="test@example.com")
        
    assert uow.committed is False


@pytest.mark.asyncio
async def test_get_user_success(user_service, uow):
    # Setup existing user
    user_id = uuid4()
    existing_user = User(username="existing", email="test@example.com", id=user_id)
    await uow.users.add(existing_user)
    
    retrieved_user = await user_service.get_user(user_id)
    assert retrieved_user.id == user_id
    assert retrieved_user.username == "existing"


@pytest.mark.asyncio
async def test_get_user_not_found(user_service):
    with pytest.raises(UserNotFoundError):
        await user_service.get_user(uuid4())
