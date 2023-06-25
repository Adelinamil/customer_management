from sqlalchemy.ext.asyncio import AsyncSession

from customer_management.exceptions.product import ProductNotFound
from customer_management.models import dto
from infrastructure.database.postgre.dao.base import BaseDAO
from infrastructure.database.postgre.models import Product


class ProductDAO(BaseDAO[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def get_by_id(self, id_: int) -> dto.Product:
        product = await self._get_by_id(id_)
        if product is None:
            raise ProductNotFound
        return product.to_dto()

    async def get_all(self) -> list[dto.Product]:
        result = await self._get_all()
        return [product.to_dto() for product in result]
