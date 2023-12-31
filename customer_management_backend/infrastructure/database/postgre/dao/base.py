from typing import Generic, Type, TypeVar, Any, Sequence
from uuid import UUID

from sqlalchemy import select, func, Row, RowMapping, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from customer_management.exceptions.base import AddModelError, MergeModelError
from customer_management.models.interfaces.dto import DTOProtocol
from infrastructure.database.postgre.models import Base

Model = TypeVar('Model', bound=Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def _get_by_id(self, id_: int | UUID | tuple,
                         options: list[ORMOption] = None) -> Model:
        return await self.session.get(self.model, id_, options=options)

    async def _get_all(self) -> Sequence[Row | RowMapping | Any]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    def save(self, obj: Model):
        self.session.add(obj)

    async def delete(self, obj: Model):
        await self.session.delete(obj)

    async def delete_all(self):
        await self.session.execute(delete(self.model))

    async def _flush(self, *objects):
        await self.session.flush(objects)

    async def count(self):
        result = await self.session.execute(
            select([func.count()]).select_from(self.model))
        return result.scalar_one()

    async def commit(self):
        await self.session.commit()

    async def _create(self, dto_obj: DTOProtocol) -> Model:
        obj = self.model.from_dto(dto_obj)
        self.save(obj)
        try:
            await self._flush(obj)
        except IntegrityError as e:
            raise AddModelError from e
        else:
            return obj

    async def _merge(self, dto_obj: DTOProtocol) -> Model:
        obj = self.model.from_dto(dto_obj)
        obj = await self.session.merge(obj)
        try:
            await self._flush(obj)
        except IntegrityError as e:
            raise MergeModelError from e
        else:
            return obj
