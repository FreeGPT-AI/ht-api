from odmantic import Field, Model, ObjectId
from odmantic.bson import BaseBSONModel
from typing import Optional

class Details(BaseBSONModel):
    """The details format for logs"""
    model: str
    success: bool
    provider_key: Optional[str] = None
    error: Optional[str] = None

class Log(Model):
    """The log document format for the database"""

    object_id: ObjectId = Field(primary_field=True)
    timestamp: int
    path: str
    ip: str
    user_key: str
    details: Details
    
    model_config = {
        "collection": "logs"
    }