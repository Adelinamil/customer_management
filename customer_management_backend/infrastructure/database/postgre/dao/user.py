from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import coalesce

from customer_management.exceptions.user import UserNotFound, UserExists
from customer_management.models import dto
from customer_management.models.enum.user import UserType
from infrastructure.database.postgre.dao.base import BaseDAO
from infrastructure.database.postgre.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_id(self, user_id: UUID) -> dto.User:
        user = await self._get_by_id(user_id)
        if user is None:
            raise UserNotFound
        return user.to_dto()

    async def get_by_username(self, username: str) -> dto.User:
        user = await self._get_by_username(username)
        return user.to_dto()

    async def get_by_username_with_password(self, username: str) -> dto.UserWithPassword:
        user = await self._get_by_username(username)
        return user.to_dto().add_password(user.password)

    async def _get_by_username(self, username: str) -> User:
        result = await self.session.execute(select(User).where(User.username == username))
        try:
            user = result.scalar_one()
        except NoResultFound as e:
            raise UserNotFound from e
        else:
            return user

    async def get_all(self) -> list[dto.User]:
        result = await self.session.execute(
            select(User)
            .order_by(coalesce(User.last_activity, datetime.fromtimestamp(0)).desc())
        )
        return [user.to_dto() for user in result.scalars().all()]

    async def create(self, user_dto: dto.UserWithPassword) -> dto.User:
        user = User.from_dto(user_dto)
        self.save(user)
        try:
            await self._flush(user)
        except IntegrityError as e:
            raise UserExists from e
        else:
            return user.to_dto()

    async def set_username(self, user: dto.User, username: str):
        db_user = await self._get_by_id(user.id)
        db_user.username = username

    async def set_password(self, user: dto.User, hashed_password: str):
        db_user = await self._get_by_id(user.id)
        db_user.password = hashed_password

    async def update_user(
            self,
            user_id: UUID,
            fields: dict,
            current_user: dto.User | None = None
    ) -> dto.User | None:
        result = await self.session.execute(
            update(User)
            .values(fields)
            .where(
                User.id == user_id,
                User.user_type.notin_({
                    current_user.user_type,
                    UserType.DEVELOPER
                }) if current_user else True
            ).returning(User)
        )
        user = result.scalar()
        return user.to_dto() if user is not None else None

    async def delete_by_id(self, user_id: UUID) -> dto.User | None:
        result = await self.session.execute(
            delete(User).where(User.id == user_id).returning(User)
        )
        user = result.scalar()
        if user:
            return user.to_dto()
