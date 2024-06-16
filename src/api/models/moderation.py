from typing import Union
from pydantic import BaseModel, field_validator
from ..utils import AIModel

class ModerationBody(BaseModel):
    """
    The default body of moderation requests
    """

    model: str
    input: Union[str, list[str]]

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Checks if a model is valid"""
        if v not in AIModel.get_all_models("moderation"):
            raise ValueError(f"Invalid model: {v}")
        return v