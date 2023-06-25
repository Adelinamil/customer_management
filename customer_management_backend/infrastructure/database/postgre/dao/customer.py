from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from customer_management.exceptions.customer import CustomerNotFound
from customer_management.models import dto
from infrastructure.database.postgre.dao.base import BaseDAO
from infrastructure.database.postgre.models import Customer


class CustomerDAO(BaseDAO[Customer]):
    def __init__(self, session: AsyncSession):
        super().__init__(Customer, session)

    async def get_by_id(self, id_: UUID) -> dto.Customer:
        customer = await self._get_by_id(id_)
        if customer is None:
            raise CustomerNotFound
        return customer.to_dto()

    async def get_all(self) -> list[dto.Customer]:
        result = await self._get_all()
        return [customer.to_dto() for customer in result]

    async def merge(self, customer_dto: dto.Customer) -> dto.Customer:
        customer = await self._merge(customer_dto)
        return customer.to_dto()

    async def delete_by_id(self, customer_id: UUID) -> dto.Customer | None:
        result = await self.session.execute(
            delete(Customer).where(Customer.id == customer_id).returning(Customer)
        )
        customer = result.scalar()
        if customer is not None:
            return customer.to_dto()
