from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from api.v1.dependencies import get_current_user, get_dao_provider, AuthProvider, get_auth_provider
from api.v1.dependencies.permissions import check_admin_type
from api.v1.models.user import UserCreate, UserUpdate
from customer_management.exceptions.user import UserExists
from customer_management.models import dto
from customer_management.models.enum.user import UserType
from infrastructure.database.holder import DAO


async def get_current_user_route(current_user: dto.User = Depends(get_current_user)) -> dto.User:
    return current_user


async def get_users(
        is_admin: bool = Depends(check_admin_type),
        dao: DAO = Depends(get_dao_provider)
) -> list[dto.User]:
    return await dao.user.get_all()


async def create_user(
        new_user: UserCreate,
        is_admin: bool = Depends(check_admin_type),
        dao: DAO = Depends(get_dao_provider),
        auth_provider: AuthProvider = Depends(get_auth_provider)
) -> bool:
    try:
        await dao.user.create(new_user.to_user_dto(auth_provider.get_password_hash))
    except UserExists as e:
        raise HTTPException(status_code=400, detail=e.message)
    else:
        await dao.commit()
        return True


async def update_user(
        user_to_update: UserUpdate,
        current_user: dto.User = Depends(get_current_user),
        is_admin: bool = Depends(check_admin_type),
        dao: DAO = Depends(get_dao_provider),
        auth_provider: AuthProvider = Depends(get_auth_provider)
):
    if user_to_update.password is not None:
        user_to_update.password = auth_provider.get_password_hash(user_to_update.password)
    updated_user = await dao.user.update_user(user_to_update.id, user_to_update.to_dict(), current_user)
    await dao.commit()
    return updated_user


async def delete_user(
        user_id: UUID,
        is_admin: bool = Depends(check_admin_type),
        dao: DAO = Depends(get_dao_provider),
) -> dto.User | None:
    deleted_user = await dao.user.delete_by_id(user_id)
    await dao.commit()
    return deleted_user


async def get_user_types(
        current_user: dto.User = Depends(get_current_user)
) -> list[str]:
    return [user_type.value for user_type in UserType]


def setup_user_routes(router: APIRouter):
    router.add_api_route('/me', get_current_user_route, methods=['GET'])
    router.add_api_route('/all', get_users, methods=['GET'])
    router.add_api_route('/types', get_user_types, methods=['GET'])
    router.add_api_route('/create', create_user, methods=['POST'])
    router.add_api_route('/update', update_user, methods=['PUT'])
    router.add_api_route('/{user_id}', delete_user, methods=['DELETE'])
