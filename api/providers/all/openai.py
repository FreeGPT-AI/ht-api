from openai import AsyncOpenAI
from typing import Union
from fastapi.responses import StreamingResponse, Response
from ...database import KeyManager
from ...responses import streaming_chat_response, normal_chat_response
from ...utils import handle_errors

class OpenAI:
    """Default OpenAI provider"""

    @classmethod
    async def _get_client(cls) -> tuple[str, AsyncOpenAI]:
        """Retrieve a valid OpenAI client and the used key"""
        key = await KeyManager.get_valid_key("openai")
        print(f"[!] Chosen key: {key}")
        return key, AsyncOpenAI(api_key=key)

    @classmethod
    @handle_errors
    async def chat_completion(cls, body: dict) -> tuple[Union[StreamingResponse, dict], str]:
        """Performs a chat completion request"""
        key, client = await cls._get_client()
        response = await client.chat.completions.create(**body)
        return await streaming_chat_response(response, body) if body.get("stream") \
            else normal_chat_response(response.choices[0].message.content, body), key

    @classmethod
    @handle_errors
    async def image(cls, body: dict) -> tuple[dict, str]:
        """Performs an image generation request"""
        key, client = await cls._get_client()
        response = await client.images.generate(**body)
        return response.model_dump(), key

    @classmethod
    @handle_errors
    async def moderation(cls, body: dict) -> tuple[dict, str]:
        """Performs a moderation request"""
        key, client = await cls._get_client()
        response = await client.moderations.create(**body)
        return response.model_dump(), key

    @classmethod
    @handle_errors
    async def embedding(cls, body: dict) -> tuple[dict, str]:
        """Performs an embedding request"""
        key, client = await cls._get_client()
        response = await client.embeddings.create(**body)
        return response.model_dump(), key

    @classmethod
    @handle_errors
    async def tts(cls, body: dict) -> tuple[Response, str]:
        """Performs a TTS request"""
        key, client = await cls._get_client()
        response = await client.audio.speech.create(**body)
        return Response(
            content=response.content,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment;filename=audio.mp3"},
            status_code=200
        ), key

    @classmethod
    @handle_errors
    async def transcriptions(cls, file: bytes) -> tuple[dict, str]:
        """Performs a transcription request"""
        key, client = await cls._get_client()
        response = await client.audio.transcriptions.create(file=file, model="whisper-1")
        return response.model_dump(), key