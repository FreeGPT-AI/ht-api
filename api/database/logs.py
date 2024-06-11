import time
import yaml
import motor.motor_asyncio as motor
from fastapi import Request

with open("values/secrets.yaml", "rb") as f:
    config = yaml.load(f)["db"]

class LogManager:
    """
    Class for writing API request logs to the MongoDB database
    """
    
    _collection = motor.AsyncIOMotorClient(config["mongo_uri"])["db"]["logs"]

    @classmethod
    async def log_api_request(cls, key: str, model: str, request: Request) -> None:
        """Logs a request and writes it to database"""

        log_info = {
            "timestamp": int(time.time()),
            "path": request.url.path,
            "user_key": request.headers.get("Authorization").replace("Bearer ", "", 1),
            "details": {
                "model": model,
                "provider_key": key,
            }
        }

        await cls._collection.insert_one(log_info)
        return