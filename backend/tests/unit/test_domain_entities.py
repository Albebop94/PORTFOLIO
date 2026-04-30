import pytest
from uuid import UUID
from src.domain.entities import User

def test_user_creation():
    user = User(username="test_user", email="test@example.com")
    
    assert user.username == "test_user"
    assert user.email == "test@example.com"
    assert isinstance(user.id, UUID)

def test_user_creation_with_id():
    custom_id = UUID("12345678-1234-5678-1234-567812345678")
    user = User(username="test_user", email="test@example.com", id=custom_id)
    
    assert user.id == custom_id
    assert user.username == "test_user"
    assert user.email == "test@example.com"
