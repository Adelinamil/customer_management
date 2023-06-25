from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from customer_management.models.enum.user import UserType


@dataclass
class User:
    id: UUID
    username: str
    user_type: UserType
    first_name: str
    second_name: str | None = None
    created: datetime | None = None
    last_activity: datetime | None = None

    @classmethod
    def from_dict(cls, dct: dict) -> User:
        return User(
            id=dct['id'],
            username=dct['username'],
            first_name=dct['first_name'],
            second_name=dct['second_name'],
            user_type=dct['user_type']
        )

    def add_password(self, hashed_password: str):
        return UserWithPassword(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            second_name=self.first_name,
            user_type=self.user_type,
            last_activity=self.last_activity,
            created=self.created,
            hashed_password=hashed_password
        )


@dataclass
class UserWithPassword(User):
    hashed_password: str | None = None

    def without_password(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            second_name=self.first_name,
            user_type=self.user_type,
            last_activity=self.last_activity,
            created=self.created
        )
