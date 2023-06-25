from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.database.holder import DAO


def get_dao_provider() -> DAO:
    raise NotImplementedError


class DatabaseProvider:
    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker

    async def dao(self):
        async with self.sessionmaker() as session:
            yield DAO(session=session)
