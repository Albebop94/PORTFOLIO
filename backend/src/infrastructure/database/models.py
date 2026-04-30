import uuid

from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities import User
from src.infrastructure.database.session import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)

    def to_domain(self) -> User:
        return User(id=self.id, username=self.username, email=self.email)

    @staticmethod
    def from_domain(user: User) -> "UserModel":
        return UserModel(id=user.id, username=user.username, email=user.email)
