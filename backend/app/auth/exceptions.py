class IncorrectCredentialsException(Exception):
    def __init__(self, status_code: int, mesaage: str):
        self.status_code = status_code
        self.message = mesaage
