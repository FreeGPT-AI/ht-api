from typing import Union, Iterable, Literal, Optional
from pydantic import BaseModel, field_validator
from ..utils import AIModel

class EmbeddingBody(BaseModel):
    """
    The default body of embedding requests
    """

    model: str
    input: Union[str, list[str], Iterable[int], Iterable[Iterable[int]]]
    dimensions: int
    encoding_format: Optional[Literal["float", "base64"]] = None

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Checks if a model is valid"""
        if v not in AIModel.get_all_models("embeddings"):
            raise ValueError(f"Invalid model: {v}")
        return v