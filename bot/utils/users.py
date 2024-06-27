import os
import string
import random
from odmantic import AIOEngine, ObjectId
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
    def _generate_key(cls) -> str:
        """Generates an API key for an user"""
        return f"ht-{''.join(random.choices(string.ascii_letters + string.digits, k=47))}"

    @classmethod
    async def create_key(cls, id: int, premium: bool = False) -> str:
        """Creates a new key for an user"""
        new_user = await cls._engine.save(User(object_id=ObjectId(), id=str(id), key=cls._generate_key(), premium=premium))
        return new_user.key

    @classmethod
    async def delete_key(cls, id: int) -> None:
        """Deletes the key of an user"""
        await cls._engine.remove(User, User.id == str(id), just_one=True)
        return

    @classmethod
    async def check_key(cls, id: int) -> Optional[User]:
        """Checks if a key exists in the database"""
        user = await cls._engine.find_one(User, User.id == str(id))
        return user
    
    @classmethod
    async def set_property(cls, id: int, property: Literal["premium", "banned"], value: bool) -> None:
        """Updates an user's property (premium or banned)"""
        user = await cls._engine.find_one(User, User.id == str(id))
        user.model_update({property: value})
        await cls._engine.save(user)
        return