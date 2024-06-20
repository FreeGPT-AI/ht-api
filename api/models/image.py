from typing import Optional, Literal
from pydantic import BaseModel, field_validator
from ..utils import AIModel

class ImageBody(BaseModel):
    """
    The default body of image requests
    """

    model: str
    prompt: str
    size: Optional[Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]] = "1024x1024"

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Checks if a model is valid"""
        if v not in AIModel.get_all_models("images.generations"):
            raise ValueError(f"Invalid model: {v}")
        return v