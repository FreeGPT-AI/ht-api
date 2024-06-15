import requests
import io
import base64
from PIL import Image
from google.generativeai import GenerativeModel, configure
from typing import Union
from fastapi.responses import StreamingResponse
from ...database import KeyManager
from ...responses import streaming_chat_response, normal_chat_response
from ...utils import handle_errors

class Gemini:
    """Default Gemini provider"""

    _safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    
    @classmethod
    def _fetch_image(cls, image_data: str):
        """Fetches an image from the given URL"""
        if image_data.startswith("data:image"):
            image_data = image_data.split(",")[1]
            decoded_image = base64.b64decode(image_data)
            return Image.open(io.BytesIO(decoded_image))
        else:
            response = requests.get(image_data, timeout=20)
            return Image.open(io.BytesIO(response.content))

    @classmethod
    def _gemini_vision_message_convert(cls, messages: list[dict[str, str]]):
        """Converts an OpenAI vision message list to the Google format"""

        payload = []

        for message in messages:
            for content_part in message.get("content", []):
                if content_part["type"] == "text":
                    text_content = content_part.get("text")
                    if text_content:
                        payload.append(text_content)
                elif content_part["type"] == "image_url":
                    image_data = content_part.get("image_url")
                    if image_data:
                        payload.append(cls._fetch_image(image_data if isinstance(image_data, str) else image_data.get("url")))

        return payload

    @classmethod
    def _gemini_message_convert(cls, messages: list[dict[str, str]]) -> list[dict[str, list]]:
        """Converts an OpenAI message list to the Google format"""

        def convert_message(message: dict[str, str]) -> list[dict[str, list]]:
            role = {"system": "user", "assistant": "model"}.get(message["role"], message["role"])
            converted = {"role": role, "parts": [{"text": message["content"]}]}
            return [converted, {"role": "model", "parts": [{"text": "Ok."}]}] if message["role"] == "system" else [converted]

        return [msg for message in messages for msg in convert_message(message)]

    @classmethod
    @handle_errors
    async def chat_completion(cls, body: dict) -> tuple[Union[StreamingResponse, dict], str]:
        """Performs a chat completion request"""

        key = await KeyManager.get_valid_key("google")
        configure(api_key=key)
        model = GenerativeModel(model_name=body["model"], safety_settings=cls._safety_settings)
        
        if any(isinstance(value, list) for value in body["messages"].values()):
            response = await model.generate_content_async(cls._gemini_vision_message_convert(body["messages"]), stream=bool(body["stream"]))
        else:
            response = await model.generate_content_async(cls._gemini_message_convert(body["messages"]), stream=bool(body["stream"]))

        return await streaming_chat_response(response, body) if body.get("stream") \
            else normal_chat_response(response.text, body), key