from typing import Literal
from pydantic import BaseModel, field_validator
from ..utils import AIModel

class TTSBody(BaseModel):
    """
    The default body of TTS requests
    """

    model: str
    input: str
    voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "alloy"

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Checks if a model is valid"""
        if v not in AIModel.get_all_models("tts"):
            raise ValueError(f"Invalid model: {v}")
        return v