from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import FileResponse

from api.v1.dependencies import get_current_user, get_dao_provider
from customer_management.exceptions.product import ProductNotFound
from customer_management.models import dto
from infrastructure.database.holder import DAO


async def get_product_image(
        product_id: int,
        dao: DAO = Depends(get_dao_provider)
):
    try:
        product = await dao.product.get_by_id(product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)

    image_path = Path(__file__).parent.parent.parent.parent / f'images/{product.image_location}'
    return FileResponse(image_path, media_type='image/jpeg')


async def get_product_by_id(
        product_id: int,
        current_user: dto.User = Depends(get_current_user),
        dao: DAO = Depends(get_dao_provider)
) -> dto.Product:
    try:
        product = await dao.product.get_by_id(product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    return product


async def get_products(
        current_user: dto.User = Depends(get_current_user),
        dao: DAO = Depends(get_dao_provider)
) -> list[dto.Product]:
    return await dao.product.get_all()


def get_product_router() -> APIRouter:
    router = APIRouter(prefix='/product', tags=['product'])
    router.add_api_route('/image/{product_id}', get_product_image, methods=['GET'])
    router.add_api_route('/all', get_products, methods=['GET'])
    router.add_api_route('/{product_id}', get_product_by_id, methods=['GET'])
    return router
