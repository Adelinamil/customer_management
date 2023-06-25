from customer_management.exceptions.base import CMBaseException


class ProductNotFound(CMBaseException):
    def __init__(self):
        super().__init__('Product not found')
