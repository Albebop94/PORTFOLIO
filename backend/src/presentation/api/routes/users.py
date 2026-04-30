from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.user_service import UserService
from src.domain.exceptions import UserAlreadyExistsError, UserNotFoundError
from src.infrastructure.database.session import get_session_factory
from src.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from src.presentation.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service() -> UserService:
    uow = SqlAlchemyUnitOfWork(get_session_factory())
    return UserService(uow)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        user = await service.create_user(username=user_in.username, email=user_in.email)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    try:
        user = await service.get_user(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
