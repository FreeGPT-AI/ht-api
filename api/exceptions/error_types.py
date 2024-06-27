from typing import Union

def get_exception_type(etype: Union[Exception, str]) -> str:
    """Returns a string representation of the exception class name"""
    class_name = etype.__class__.__name__.replace("Exception", "Error")
    return "".join([f"_{i.lower()}" if i.isupper() else i for i in class_name]).lstrip("_")

class BaseException(Exception):
    """
    Base class for all response exceptions in this project
    """

    def __init__(self, message: str, status: int = None, type: str = None) -> None:
        self.message = message
        self.type = get_exception_type(self) if not type else type
        self.status = status

class InvalidRequestException(BaseException):
    """Exception for invalid requests"""
    pass

class InvalidResponseException(BaseException):
    """Exception for invalid responses"""
    pass