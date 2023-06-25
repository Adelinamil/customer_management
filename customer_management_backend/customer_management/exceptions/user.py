from customer_management.exceptions.base import CMBaseException


class UserException(CMBaseException):
    def __init__(self, msg: str = 'Some user exception'):
        super().__init__(msg)


class UserNotFound(UserException):
    def __init__(self):
        super().__init__('Incorrect username or password')


class UserExists(UserException):
    def __init__(self):
        super().__init__('User already exists')
