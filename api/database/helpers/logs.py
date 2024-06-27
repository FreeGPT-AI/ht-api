import os
import time
from odmantic import AIOEngine, ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request
from ..models import Log, Details

class LogManager:
    """
    Class for writing API request logs to the MongoDB database
    """
    
    _engine = AIOEngine(
        client=AsyncIOMotorClient(os.environ["MONGO_URI"]),
        database="db"
    )

    @classmethod
    async def log_api_request(cls, model: str, request: Request, success: bool, error: str = None, key: str = None) -> None:
        """Logs a request and writes it to database"""

        log_info = Log(
            object_id=ObjectId(),
            timestamp=int(time.time()),
            path=request.url.path,
            ip=request.client.host,
            user_key=request.headers.get("Authorization").replace("Bearer ", "", 1),
            details=Details(
                model=model,
                provider_key=key,
                success=success,
                error=error
            )
        )

        await cls._engine.save(log_info)
        return