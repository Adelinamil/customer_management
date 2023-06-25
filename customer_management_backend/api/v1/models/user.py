from typing import Callable
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, constr

from customer_management.models import dto
from customer_management.models.enum.user import UserType


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=32)
    first_name: constr(min_length=2, max_length=50)
    password: constr(min_length=5, max_length=32)
    second_name: str = Field(default=None, max_length=50)
    user_type: UserType

    def to_user_dto(self, hash_func: Callable) -> dto.UserWithPassword:
        return dto.UserWithPassword(
            id=uuid4(),
            username=self.username,
            hashed_password=hash_func(self.password),
            first_name=self.first_name,
            second_name=self.second_name,
            user_type=self.user_type
        )


class UserUpdate(BaseModel):
    id: UUID
    username: str | None = Field(default=None, min_length=3, max_length=32)
    password: str | None = Field(min_length=5, max_length=32)
    first_name: str | None = Field(min_length=2, max_length=100)
    second_name: str | None = Field(default=None, min_length=2, max_length=100)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.dict().items() if v is not None and k != 'id'}
