import time
import orjson
from fastapi.responses import StreamingResponse
from google.generativeai.types import AsyncGenerateContentResponse
from collections.abc import AsyncGenerator
from typing import Union, Any
from .pretty_json import PrettyJSONResponse
from ..utils import gen_system_fingerprint, gen_completion_id, handle_errors, tokenize

def generate_chunk(chunk: str, model: str) -> dict[str, Union[str, list, float]]:
    """Generates a chunk of a chat response"""
    return {
        "id": gen_completion_id(),
        "object": "chat.completion",
        "system_fingerprint": gen_system_fingerprint(),
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {
                    "role": "assistant",
                    "content": chunk
                }
            }
        ]
    }

async def generate_response(response: Union[str, Any], data: dict) -> AsyncGenerator[bytes]:
    """Generates a response and returns a bytes async generator"""
    try:
        if isinstance(response, str):
            for chunk in response:
                yield b"data: " + orjson.dumps(generate_chunk(chunk, data["model"])) + b"\n\n"
        elif isinstance(response, AsyncGenerateContentResponse):
            async for chunk in response:
                yield b"data: " + orjson.dumps(generate_chunk(chunk.text, data["model"])) + b"\n\n"
        else:
            async for chunk in response:
                yield b"data: " + chunk.model_dump_json().encode("utf-8") + b"\n\n"
    finally:
        yield b"data: [DONE]\n\n"

@handle_errors
async def streaming_chat_response(response: Union[str, Any], data: dict) -> StreamingResponse:
    """Streaming response generator"""
    return StreamingResponse(generate_response(response, data), media_type="text/event-stream")

def normal_chat_response(response: str, body: dict) -> PrettyJSONResponse:
    """Non-streaming response generator"""
    
    try:
        prompt_tokens = tokenize("".join([message["content"] for message in body["messages"]]))
        completion_tokens = tokenize(response)
    except:
        prompt_tokens = 0
        completion_tokens = 0
    
    return {
        "id": gen_completion_id(),
        "object": "chat.completion",
        "system_fingerprint": gen_system_fingerprint(),
        "created": int(time.time()),
        "model": body["model"],
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": response},
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens
        }
    }