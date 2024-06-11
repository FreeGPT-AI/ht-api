from typing import Optional
from pydantic import BaseModel, field_validator

class AdminBody(BaseModel):
    """
    The default body of admin requests
    """

    id: int
    action: str
    status: Optional[bool] = None
    property: Optional[str] = None

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        """Checks if an action is valid"""
        if v not in ["create", "get", "update", "delete"]:
            raise ValueError(f"Invalid action: {v}")
        return v