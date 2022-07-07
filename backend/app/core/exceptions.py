from fastapi import status


class IncorrectCredentialsException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class UserNotFound(Exception):
    def __init__(self, message: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = message


class UserAlreadyExists(Exception):
    def __init__(self, message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message


class IncorrectFormData(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class NotFound(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
