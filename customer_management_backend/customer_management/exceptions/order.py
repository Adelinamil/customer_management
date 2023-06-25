from customer_management.exceptions.base import CMBaseException


class OrderNotFound(CMBaseException):
    def __init__(self):
        super().__init__('Order not found')
