from openai import AsyncOpenAI
from typing import Union
from fastapi.responses import StreamingResponse
from ...database import KeyManager
from ...responses import streaming_chat_response, normal_chat_response
from ...utils import handle_errors

class Anthropic:
    """
    Default Anthropic provider
    """

    @classmethod
    async def _get_client(cls) -> tuple[str, AsyncOpenAI]:
        """Retrieve a valid OpenAI client and the used key"""
        key = await KeyManager.get_valid_key("openrouter")
        print(f"[!] Chosen key: {key}")
        return key, AsyncOpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")

    @classmethod
    @handle_errors
    async def chat_completion(cls, body: dict) -> tuple[Union[StreamingResponse, dict], str]:
        """Performs a chat completion request"""
        key, client = await cls._get_client()
        body["model"] = f"anthropic/{body.get('model', '')}"
        response = await client.chat.completions.create(**body)
        body["model"] = body.get("model").replace("anthropic/", "")
        return await streaming_chat_response(response, body) if body.get("stream") \
            else normal_chat_response(response.choices[0].message.content, body), key