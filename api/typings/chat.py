from typing import Union, Optional, Any, Iterable, Literal
from pydantic import BaseModel, field_validator
from ..utils import AIModel

class ChatBody(BaseModel):
    """
    The default body of chat requests
    """

    model: str
    messages: list[dict[str, Union[str, list]]]
    stream: bool = False
    temperature: Union[float, int] = 1
    top_p: Union[float, int] = 1
    presence_penalty: Union[float, int] = 0
    frequency_penalty: Union[float, int] = 0
    tools: Optional[Iterable[Any]] = None
    tool_choice: Optional[Union[Literal["none", "auto", "required"], Any]] = None

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Checks if a model is valid"""
        if v not in AIModel.get_all_models("chat.completions"):
            raise ValueError(f"Invalid model: {v}")
        return v