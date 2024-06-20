import os
import time
import yaml
import motor.motor_asyncio as motor
from fastapi import Request

class LogManager:
    """
    Class for writing API request logs to the MongoDB database
    """
    
    _collection = motor.AsyncIOMotorClient(os.environ["MONGO_URI"])["db"]["logs"]

    @classmethod
    async def log_api_request(cls, model: str, request: Request, success: bool, error: str = None, key: str = None) -> None:
        """Logs a request and writes it to database"""

        log_info = {
            "timestamp": int(time.time()),
            "path": request.url.path,
            "ip": request.headers.get("CF-Connecting-IP"),
            "user_key": request.headers.get("Authorization").replace("Bearer ", "", 1),
            "details": {
                "model": model,
                "provider_key": key,    
                "success": success,
                "error": error
            }
        }

        await cls._collection.insert_one(log_info)
        return