import os
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Literal, Optional
from ..models import User

class UserManager:
    """
    Class for handling user-related data in the MongoDB database
    """
    
    _engine = AIOEngine(
        client=AsyncIOMotorClient(os.environ["MONGO_URI"]),
        database="db"
    )

    @classmethod
    async def check_key(cls, key: str) -> Optional[User]:
        """Checks if a key exists in the database"""
        user = await cls._engine.find_one(User, User.key == key)
        return user
    
    @classmethod
    async def get_property(cls, key: str, property: Literal["premium", "banned"]) -> Optional[bool]:
        """Gets an user's property (premium or banned)"""
        user = await cls._engine.find_one(User, User.key == key)
        return getattr(user, property) if user else None