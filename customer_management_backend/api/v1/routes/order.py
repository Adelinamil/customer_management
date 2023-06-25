from fastapi import APIRouter, Depends, HTTPException

from api.v1.dependencies import get_current_user, get_dao_provider
from customer_management.exceptions.order import OrderNotFound
from customer_management.models import dto
from infrastructure.database.holder import DAO


async def get_order_by_id(
        order_id: int,
        current_user: dto.User = Depends(get_current_user),
        dao: DAO = Depends(get_dao_provider)
) -> dto.Order:
    try:
        order = await dao.order.get_by_id(order_id)
    except OrderNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return order


async def get_orders(
        current_user: dto.User = Depends(get_current_user),
        dao: DAO = Depends(get_dao_provider)
) -> list[dto.Order]:
    return await dao.order.get_all()


def get_order_router() -> APIRouter:
    router = APIRouter(prefix='/order', tags=['order'])
    router.add_api_route('/all', get_orders, methods=['GET'])
    router.add_api_route('/{order_id}', get_order_by_id, methods=['GET'])
    return router
