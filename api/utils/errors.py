import traceback
from typing import Union, Callable
from fastapi import Request
from fastapi.responses import Response
from fastapi.exceptions import HTTPException, RequestValidationError
from ..exceptions import BaseException, InvalidRequestException, InvalidResponseException
from . import make_error_response

def configure_error_handlers() -> dict[Union[type, Exception, int], Callable]:
    """Returns a dict of error handlers"""

    def status_404_handler(request: Request, _: Exception) -> Response:
        """Not found page error handler"""
        return make_error_response(
            message=f"Invalid URL ({request.method} {request.url.path})",
            type="invalid_request_error",
            status=404
        )

    def status_405_handler(request: Request, _: Exception) -> Response:
        """Method not allowed error handler"""
        return make_error_response(
            message=f"Not allowed to {request.method} on {request.url.path}.",
            type="invalid_request_error",
            status=405
        )

    def exception_handler(_: Request, exc: Union[Exception, BaseException]) -> Response:
        """Generic error handler"""
        traceback.print_exc()
        return make_error_response(
            message=exc.message if isinstance(exc, BaseException) else f"An unexpected error has occurred: {exc}",
            type=exc.type if isinstance(exc, BaseException) else "base_error",
            status=exc.status if isinstance(exc, BaseException) else 500
        )

    def validation_error_handler(_: Request, exc: RequestValidationError) -> Response:
        """Validation error handler"""
        message = ", ".join(e["msg"] for e in exc.errors()).replace("Value error, ", "")
        return make_error_response(
            message=message,
            type="invalid_request_error",
            status=422 if "Invalid model" not in message else 404
        )

    def http_exception_handler(_: Request, exc: Union[InvalidRequestException, InvalidResponseException]) -> Response:
        """HTTP exception handler"""
        return make_error_response(
            message=exc.message,
            type=exc.type,
            status=exc.status
        )

    return {
        404: status_404_handler,
        405: status_405_handler,
        Exception: exception_handler,
        BaseException: exception_handler,
        ValueError: exception_handler,
        InvalidRequestException: http_exception_handler,
        InvalidResponseException: http_exception_handler,
        HTTPException: http_exception_handler,
        RequestValidationError: validation_error_handler
    }