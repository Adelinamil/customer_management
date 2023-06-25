from enum import Enum


class UserType(Enum):
    SELLER = 'seller'
    MANAGER = 'manager'
    ADMIN = 'admin'
    DEVELOPER = 'developer'
