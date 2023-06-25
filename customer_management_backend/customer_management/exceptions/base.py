class CMBaseException(Exception):
    def __init__(self, msg: str = 'Base exception'):
        self.message = msg
        super().__init__(msg)


class MergeModelError(CMBaseException):
    def __init__(self):
        super().__init__('Can\'t merge model')


class AddModelError(CMBaseException):
    def __init__(self):
        super().__init__('Can\'t create model')
