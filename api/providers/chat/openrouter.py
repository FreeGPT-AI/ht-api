from openai import AsyncOpenAI
from typing import Union
from fastapi.responses import StreamingResponse
from ...database import KeyManager
from ...responses import streaming_chat_response, normal_chat_response
from ...utils import handle_errors

class OpenRouter:
    """
    Default OpenRouter provider
    """
    
    _model_map = {
        "claude-3-haiku": "anthropic/claude-3-haiku:beta",
        "claude-3-sonnet": "anthropic/claude-3-sonnet:beta",
        "claude-3-opus": "anthropic/claude-3-opus:beta",
        "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet:beta",
        "llama-2-13b": "meta-llama/llama-2-13b-chat",
        "llama-2-70b": "meta-llama/llama-2-70b-chat",
        "llama-3-8b": "meta-llama/llama-3-8b-instruct",
        "llama-3-70b": "meta-llama/llama-3-70b-instruct"
    }
    
    @classmethod
    async def _get_client(cls) -> tuple[str, AsyncOpenAI]:
        """Retrieve a valid OpenAI client"""
        key = await KeyManager.get_valid_key("openrouter")
        print(f"[!] Chosen key: {key}")
        return key, AsyncOpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")

    @classmethod
    @handle_errors
    async def chat_completion(cls, body: dict) -> tuple[Union[StreamingResponse, dict], str]:
        """Performs a chat completion request"""
        key, client = await cls._get_client()
        body["model"] = cls._model_map[body["model"]]
        response = await client.chat.completions.create(**dict(list(body.items())[:3]))
        body["model"] = body["model"].split("/")[1]
        return await streaming_chat_response(response, body) if body.get("stream") \
            else normal_chat_response(response.choices[0].message.content, body), key
