from dataclasses import dataclass, field
from typing import Union, Coroutine, Any
from ..providers import (
    OpenAI,
    OpenRouter,
    MistralAI,
    Gemini,
    Perplexity,
    StableDiffusion
)

@dataclass
class AIModel:
    """
    Dataclass for handling AI model-related data
    """

    id: str
    object: str = "model"
    created: int = 0
    owned_by: str = "openai"
    type: str = "chat.completions"
    premium: bool = False
    endpoint: str = "/v1/chat/completions"
    providers: list = field(default_factory=list)
    _provider_index: int = field(default=0, init=False, repr=False)

    def to_json(self, full: bool = True) -> dict[str, Union[str, int, list, bool]]:
        """Returns a JSON representation of an AI model (and its provider if specified)"""
        model_object = self.__dict__.copy()
        del model_object["providers"]
        model_object.pop("_provider_index", None)
        return model_object if not full else self.__dict__.copy()

    @classmethod
    def all_to_json(cls) -> dict[str, Union[str, int, bool]]:
        """Returns a JSON representation of the list of available AI models"""
        return {"object": "list", "data": [model.to_json(False) for model in AIModels.models.values()]}

    @classmethod
    def get_all_models(cls, type: str, premium: bool = False) -> list[str]:
        """Returns a list of all available AI models IDs, filtered by type and premium status"""
        return [model["id"] for model in cls.all_to_json()["data"] 
                if model["type"] == type and (not premium or model["premium"] == True)]

    @classmethod
    def get_provider(cls, model: str) -> Coroutine[Any, Any, Any]:
        """Returns a provider for the given AI model using round-robin load balancing"""
        ai_model = AIModels.models[model]
        provider = ai_model.providers[ai_model._provider_index]
        ai_model._provider_index = (ai_model._provider_index + 1) % len(ai_model.providers)
        return provider

class AIModelMeta(type):
    """
    Metaclass for the AIModel class that initializes and registers AI models
    """

    def __init__(cls, name, bases, attrs) -> None:
        super().__init__(name, bases, attrs)
        cls.models = {value.id: value for value in attrs.values() if isinstance(value, AIModel)}

class AIModels(metaclass=AIModelMeta):
    """
    Class for registering and managing AI models
    """

    gpt_3_5_turbo = AIModel(
        id="gpt-3.5-turbo",
        providers=[OpenAI.chat_completion]
    )
    gpt_3_5_turbo_16k = AIModel(
        id="gpt-3.5-turbo-16k",
        providers=[OpenAI.chat_completion]
    )
    gpt_3_5_turbo_1106 = AIModel(
        id="gpt-3.5-turbo-1106",
        providers=[OpenAI.chat_completion]
    )
    gpt_3_5_turbo_0125 = AIModel(
        id="gpt-3.5-turbo-0125",
        providers=[OpenAI.chat_completion]
    )
    gpt_4 = AIModel(
        id="gpt-4",
        providers=[OpenAI.chat_completion]
    )
    gpt_4_1106_preview = AIModel(
        id="gpt-4-1106-preview",
        premium=True,
        providers=[OpenAI.chat_completion]
    )
    gpt_4_0125_preview = AIModel(
        id="gpt-4-0125-preview",
        premium=True,
        providers=[OpenAI.chat_completion]
    )
    gpt_4_turbo_preview = AIModel(
        id="gpt-4-turbo-preview",
        premium=True,
        providers=[OpenAI.chat_completion]
    )
    gpt_4_turbo = AIModel(
        id="gpt-4-turbo",
        premium=True,
        providers=[OpenAI.chat_completion]
    )
    gpt_4_turbo_2024_04_09 = AIModel(
        id="gpt-4-turbo-2024-04-09",
        premium=True,
        providers=[OpenAI.chat_completion]
    )
    gpt_4o = AIModel(
        id="gpt-4o",
        premium=True,
        providers=[OpenAI.chat_completion]
    )
    gpt_4o_2024_05_13 = AIModel(
        id="gpt-4o-2024-05-13",
        premium=True,
        providers=[OpenAI.chat_completion]
    )
    claude_3_haiku = AIModel(
        id="claude-3-haiku",
        owned_by="anthropic",
        providers=[OpenRouter.chat_completion]
    )
    claude_3_sonnet = AIModel(
        id="claude-3-sonnet",
        owned_by="anthropic",
        premium=True,
        providers=[OpenRouter.chat_completion]
    )
    claude_3_opus = AIModel(
        id="claude-3-opus",
        owned_by="anthropic",
        premium=True,
        providers=[OpenRouter.chat_completion]
    )
    claude_3_5_sonnet = AIModel(
        id="claude-3.5-sonnet",
        owned_by="anthropic",
        premium=True,
        providers=[OpenRouter.chat_completion]
    )
    gemini_pro = AIModel(
        id="gemini-pro",
        type="chat.completions",
        owned_by="google",
        providers=[Gemini.chat_completion]
    )
    gemini_1_5_flash = AIModel(
        id="gemini-1.5-flash",
        type="chat.completions",
        owned_by="google",
        providers=[Gemini.chat_completion]
    )
    gemini_1_5_pro = AIModel(
        id="gemini-1.5-pro",
        type="chat.completions",
        owned_by="google",
        providers=[Gemini.chat_completion]
    )
    open_mistral_7b = AIModel(
        id="open-mistral-7b",
        type="chat.completions",
        owned_by="mistralai",
        providers=[MistralAI.chat_completion]
    )
    open_mixtral_8x7b = AIModel(
        id="open-mixtral-8x7b",
        type="chat.completions",
        owned_by="mistralai",
        providers=[MistralAI.chat_completion]
    )
    open_mixtral_8x22b = AIModel(
        id="open-mixtral-8x22b",
        type="chat.completions",
        owned_by="mistralai",
        providers=[MistralAI.chat_completion]
    )
    mistral_small = AIModel(
        id="mistral-small-latest",
        type="chat.completions",
        owned_by="mistralai",
        providers=[MistralAI.chat_completion]
    )
    mistral_medium = AIModel(
        id="mistral-medium-latest",
        type="chat.completions",
        owned_by="mistralai",
        providers=[MistralAI.chat_completion]
    )
    mistral_large = AIModel(
        id="mistral-large-latest",
        type="chat.completions",
        owned_by="mistralai",
        providers=[MistralAI.chat_completion]
    )
    llama_2_13b = AIModel(
        id="llama-2-13b",
        type="chat.completions",
        owned_by="meta",
        providers=[OpenRouter.chat_completion]
    )
    llama_2_70b = AIModel(
        id="llama-2-70b",
        type="chat.completions",
        owned_by="meta",
        providers=[OpenRouter.chat_completion]
    )
    llama_3_8b = AIModel(
        id="llama-3-8b",
        type="chat.completions",
        owned_by="meta",
        providers=[OpenRouter.chat_completion]
    )
    llama_3_70b = AIModel(
        id="llama-3-70b",
        type="chat.completions",
        owned_by="meta",
        providers=[OpenRouter.chat_completion]
    )
    llama_3_sonar_small_32k_chat = AIModel(
        id="llama-3-sonar-small-32k-chat",
        type="chat.completions",
        owned_by="perplexity",
        providers=[Perplexity.chat_completion]
    )
    llama_3_sonar_small_32k_online = AIModel(
        id="llama-3-sonar-small-32k-online",
        type="chat.completions",
        owned_by="perplexity",
        providers=[Perplexity.chat_completion]
    )
    llama_3_sonar_large_32k_chat = AIModel(
        id="llama-3-sonar-large-32k-chat",
        type="chat.completions",
        owned_by="perplexity",
        providers=[Perplexity.chat_completion]
    )
    llama_3_sonar_large_32k_online = AIModel(
        id="llama-3-sonar-large-32k-chat",
        type="chat.completions",
        owned_by="perplexity",
        providers=[Perplexity.chat_completion]
    )
    dall_e_3 = AIModel(
        id="dall-e-3",
        type="images.generations",
        premium=True,
        providers=[OpenAI.image],
        endpoint="/v1/images/generations"
    )
    sdxl = AIModel(
        id="sdxl",
        type="images.generations",
        owned_by="stable-diffusion",
        providers=[StableDiffusion.image],
        endpoint="/v1/images/generations"
    )
    stable_diffusion_3 = AIModel(
        id="stable-diffusion-3",
        type="images.generations",
        owned_by="stable-diffusion",
        providers=[StableDiffusion.image],
        endpoint="/v1/images/generations"
    )
    text_moderation_latest = AIModel(
        id="text-moderation-latest",
        type="moderations",
        providers=[OpenAI.moderation],
        endpoint="/v1/moderations"
    )
    text_moderation_stable = AIModel(
        id="text-moderation-stable",
        type="moderations",
        providers=[OpenAI.moderation],
        endpoint="/v1/moderations"
    )
    text_embedding_3_small = AIModel(
        id="text-embedding-3-small",
        type="embeddings",
        providers=[OpenAI.embedding],
        endpoint="/v1/embeddings"
    )
    text_embedding_3_large = AIModel(
        id="text-embedding-3-large",
        type="embeddings",
        premium=True,
        providers=[OpenAI.embedding],
        endpoint="/v1/embeddings"
    )
    tts_1 = AIModel(
        id="tts-1",
        type="audio.speech",
        providers=[OpenAI.tts],
        endpoint="/v1/audio/speech"
    )
    tts_1_hd = AIModel(
        id="tts-1-hd",
        type="audio.speech",
        premium=True,
        providers=[OpenAI.tts],
        endpoint="/v1/audio/speech"
    )
    whisper_1 = AIModel(
        id="whisper-1",
        type="audio.transcriptions",
        providers=[OpenAI.transcriptions],
        endpoint="/v1/audio/transcriptions"
    )
