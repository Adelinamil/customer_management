from fastapi import Depends, HTTPException

from api.v1.dependencies import get_current_user
from customer_management.models import dto
from customer_management.models.enum.user import UserType


async def check_admin_type(user: dto.User = Depends(get_current_user)) -> bool:
    if user.user_type not in (UserType.ADMIN, UserType.DEVELOPER):
        raise HTTPException(status_code=403)
    return True


async def check_developer_type(user: dto.User = Depends(get_current_user)) -> bool:
    if user.user_type.value not in (UserType.DEVELOPER,):
        raise HTTPException(status_code=403)
    return True
