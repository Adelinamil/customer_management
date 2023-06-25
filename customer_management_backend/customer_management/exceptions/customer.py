from customer_management.exceptions.base import CMBaseException


class CustomerNotFound(CMBaseException):
    def __init__(self):
        super().__init__('Customer not found')
