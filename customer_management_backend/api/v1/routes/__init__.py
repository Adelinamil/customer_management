from fastapi import APIRouter

from api.v1.dependencies import AuthProvider
from api.v1.routes.customer import get_customer_router
from api.v1.routes.order import get_order_router
from api.v1.routes.product import get_product_router
from api.v1.routes.user import setup_user_routes


def setup_routers(api_router: APIRouter, auth_provider: AuthProvider):
    user_router = APIRouter(prefix='/user', tags=['user'])
    auth_provider.setup_auth_routes(user_router)
    setup_user_routes(user_router)
    api_router.include_router(user_router)
    api_router.include_router(get_product_router())
    api_router.include_router(get_order_router())
    api_router.include_router(get_customer_router())
