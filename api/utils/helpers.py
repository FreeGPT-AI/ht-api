import random
import string
import openai
import traceback
import ujson
import tiktoken
from fastapi.responses import StreamingResponse, Response
from typing import Union, Any, Coroutine

def gen_random_string(prefix: str, length: int = 29, charset: str = string.ascii_letters + string.digits) -> str:
    """Generates a random string with a given prefix and length"""
    return prefix + "".join(random.choices(charset, k=length))

def gen_completion_id() -> str:
    """Generates a chat completion ID"""
    return gen_random_string("chatcmpl-")

def gen_system_fingerprint() -> str:
    """Generates a system fingerprint"""
    return gen_random_string("fp_", length=10, charset=string.ascii_lowercase + string.digits)

def make_error_response(message: str, type: str, status: int) -> Response:
    """Sets up the response for an error"""
    return Response(
        content=ujson.dumps(
            {"error": {"message": message, "type": type, "param": None, "code": None}},
            indent=4,
            escape_forward_slashes=False
        ),
        status_code=status,
        media_type="application/json"
    )

def handle_errors(func: Coroutine[Any, Any, Any]) -> Coroutine[Any, Any, Union[Response, StreamingResponse, tuple]]:
    """Decorator to handle errors for a provider"""
    
    async def wrapper(*args, **kwargs) -> Union[Response, StreamingResponse, tuple]:
        """Wrapper function to handle errors"""
        try:
            return await func(*args, **kwargs)
        except (TypeError, openai.APIError) as e:
            traceback.print_exc()
            return make_error_response(
                message="We were unable to generate a response. Please try again later.",
                type="invalid_response_error",
                status=500
            ), str(e), False
    
    return wrapper

def tokenize(text: str) -> int:
    """Tokenizes a string using the tiktoken library"""
    encoding = tiktoken.get_encoding("cl100k_base")
    encoded_text = encoding.encode(text)
    return len(encoded_text)