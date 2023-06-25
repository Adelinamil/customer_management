from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgre.dao.customer import CustomerDAO
from infrastructure.database.postgre.dao.order import OrderDAO
from infrastructure.database.postgre.dao.product import ProductDAO
from infrastructure.database.postgre.dao.user import UserDAO


class DAO:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.customer = CustomerDAO(self.session)
        self.user = UserDAO(self.session)
        self.product = ProductDAO(self.session)
        self.order = OrderDAO(self.session)

    async def commit(self):
        await self.session.commit()
