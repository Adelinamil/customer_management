from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from api.config import Config
from api.v1.dependencies.auth import AuthProvider, get_current_user, get_auth_provider
from api.v1.dependencies.database import DatabaseProvider, get_dao_provider


def setup(
        app: FastAPI,
        db_sessionmaker: async_sessionmaker,
        config: Config
):
    db_provider = DatabaseProvider(sessionmaker=db_sessionmaker)
    auth_provider = AuthProvider(config.auth)

    app.dependency_overrides[get_dao_provider] = db_provider.dao  # noqa
    app.dependency_overrides[get_current_user] = auth_provider.get_current_user  # noqa
    app.dependency_overrides[get_auth_provider] = lambda: auth_provider  # noqa
