import logging

import uvicorn
from fastapi import FastAPI, APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from starlette.middleware.cors import CORSMiddleware

from api import v1
from api.v1.dependencies import get_auth_provider
from .config import load_config


def main():
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    # Подключение к PostgreSQL
    engine = create_async_engine(url=config.db.make_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    app = FastAPI()
    api_router_v1 = APIRouter(prefix='/v1')
    v1.dependencies.setup(app, async_session, config)
    v1.routes.setup_routers(api_router_v1, app.dependency_overrides[get_auth_provider]())  # noqa

    main_api_router = APIRouter(prefix='/api')
    main_api_router.include_router(api_router_v1)
    app.include_router(main_api_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
