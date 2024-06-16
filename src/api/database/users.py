import yaml
import motor.motor_asyncio as motor
from typing import Literal, Union, Optional
from ..utils import gen_random_string

with open("values/secrets.yml", "r") as f:
    config = yaml.safe_load(f)["db"]

class UserManager:
    """
    Class for handling user-related data in the MongoDB database
    """
    
    _collection = motor.AsyncIOMotorClient(config["mongo_uri"])["db"]["users"]
    
    @classmethod
    async def create_key(cls, user_id: int) -> str:
        """Creates a new key for an user"""
        key = gen_random_string("ht-", length=47)
        await cls._collection.insert_one({"id": str(user_id), "key": key, "banned": False, "premium": False})
        return key

    @classmethod
    async def delete_key(cls, user_id: int) -> None:
        """Deletes the key of an user"""
        await cls._collection.delete_one({"id": str(user_id)})
        return

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional[dict[str, Union[str, bool]]]:
        """Returns an user by its ID"""
        user = await cls._collection.find_one({"id": str(user_id)})
        return user

    @classmethod
    async def check_key(cls, key: str = None) -> Optional[dict]:
        """Checks if a key exists in the database"""
        user = await cls._collection.find_one({"key": key})
        return user
    
    @classmethod
    async def get_property(cls, key: str, property: Literal["premium", "banned"]) -> Optional[bool]:
        """Gets an user"s property (premium or banned)"""
        user = await cls._collection.find_one({"key": key})
        return user.get(property) if user else None
    
    @classmethod
    async def set_property(cls, user_id: int, property: Literal["premium", "banned"], value: bool) -> None:
        """Updates an user's property (premium or banned)"""
        await cls._collection.find_one_and_update({"id": str(user_id)}, {"$set": {property: value}})
        return