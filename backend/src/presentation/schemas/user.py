from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}
