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
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    @classmethod
    def _gemini_message_convert(cls, old_messages: list[dict[str, str]]) -> list[dict[str, list]]:
        """Converts an OpenAI-compatible message list to the Gemini format"""

        def convert_message(message):
            role = {"system": "user", "assistant": "model"}.get(message["role"], message["role"])
            converted = {"role": role, "parts": [{"text": message["content"]}]}
            return [converted, {"role": "model", "parts": [{"text": "Ok."}]}] if message["role"] == "system" else [converted]

        return [msg for message in old_messages for msg in convert_message(message)]

    @classmethod
    @handle_errors
    async def chat_completion(cls, body: dict) -> tuple[Union[StreamingResponse, dict], str]:
        """Performs a chat completion request"""

        key = await KeyManager.get_valid_key("google")
        print(f"[!] Chosen key: {key}")
        configure(api_key=key)

        model = GenerativeModel(model_name=body.get("model"), safety_settings=cls._safety_settings)
        response = await model.generate_content_async(cls._gemini_message_convert(body["messages"]), stream=bool(body.get("stream")))

        return await streaming_chat_response(response, body) if body.get("stream") \
            else normal_chat_response(response.text, body), key