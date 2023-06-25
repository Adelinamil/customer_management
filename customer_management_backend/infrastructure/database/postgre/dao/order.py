from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from customer_management.exceptions.order import OrderNotFound
from customer_management.models import dto
from infrastructure.database.postgre.dao.base import BaseDAO
from infrastructure.database.postgre.models import Order


class OrderDAO(BaseDAO[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    async def get_by_id(self, id_: int) -> dto.Order:
        order = await self._get_by_id(
            id_,
            [joinedload(Order.customer), joinedload(Order.product)]
        )
        if order is None:
            raise OrderNotFound
        return order.to_dto()

    async def get_all(self) -> list[dto.Order]:
        result = await self.session.execute(
            select(Order)
            .order_by(Order.dt.desc())
            .options(joinedload(Order.customer), joinedload(Order.product))
        )
        return [order.to_dto() for order in result.scalars().all()]
