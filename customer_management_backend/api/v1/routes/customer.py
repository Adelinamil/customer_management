from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.v1.dependencies import get_current_user, get_dao_provider
from api.v1.dependencies.permissions import check_admin_type
from api.v1.models.customer import CustomerUpdate
from customer_management.exceptions.customer import CustomerNotFound
from customer_management.models import dto
from infrastructure.database.holder import DAO


async def get_customer_by_id(
        customer_id: UUID,
        current_user: dto.User = Depends(get_current_user),
        dao: DAO = Depends(get_dao_provider)
) -> dto.Customer:
    try:
        customer = await dao.customer.get_by_id(customer_id)
    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return customer


async def get_customers(
        current_user: dto.User = Depends(get_current_user),
        dao: DAO = Depends(get_dao_provider)
) -> list[dto.Customer]:
    return await dao.customer.get_all()


async def update_customer(
        customer: CustomerUpdate,
        is_admin: bool = Depends(check_admin_type),
        dao: DAO = Depends(get_dao_provider)
) -> dto.Customer:
    updated_customer = await dao.customer.merge(dto.Customer.from_dict(customer.dict()))
    await dao.commit()
    return updated_customer


async def delete_customer(
        customer_id: UUID,
        is_admin: bool = Depends(check_admin_type),
        dao: DAO = Depends(get_dao_provider)
) -> dto.Customer | None:
    deleted_customer = await dao.customer.delete_by_id(customer_id)
    await dao.commit()
    return deleted_customer


def get_customer_router() -> APIRouter:
    router = APIRouter(prefix='/customer', tags=['customer'])
    router.add_api_route('/all', get_customers, methods=['GET'])
    router.add_api_route('/update', update_customer, methods=['PUT'])
    router.add_api_route('/{customer_id}', delete_customer, methods=['DELETE'])
    router.add_api_route('/{customer_id}', get_customer_by_id, methods=['GET'])
    return router
