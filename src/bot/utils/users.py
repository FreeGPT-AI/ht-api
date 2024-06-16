import yaml
import string
import random
import motor.motor_asyncio as motor
from typing import Literal, Union, Optional

with open("values/secrets.yml", "r") as f:
    config = yaml.safe_load(f)["db"]

class UserManager:
    """
    Class for handling user-related data in the MongoDB database using PyMongo and Asgiref
    """
    
    collection = motor.AsyncIOMotorClient(config["mongo_uri"])["db"]["users"]

    @classmethod
    def gen_random_string(cls, prefix: str, length: int = 29, charset: str = string.ascii_letters + string.digits) -> str:
        """Generates a random string with a given prefix and length"""
        return prefix + "".join(random.choices(charset, k=length))

    @classmethod
    async def create_key(cls, user_id: int) -> str:
        """Creates a new key for an user"""
        key = cls.gen_random_string("ht-", length=47)
        await cls.collection.insert_one({"id": str(user_id), "key": key, "banned": False, "premium": False})
        return key

    @classmethod
    async def delete_key(cls, user_id: int) -> None:
        """Deletes the key of an user"""
        await cls.collection.delete_one({"id": str(user_id)})
        return

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional[dict[str, Union[str, bool]]]:
        """Returns an user by its ID"""
        user = await cls.collection.find_one({"id": str(user_id)})
        return user

    @classmethod
    async def check_key(cls, key: str = None) -> Optional[dict]:
        """Checks if a key exists in the database"""
        user = await cls.collection.find_one({"key": key})
        return user
    
    @classmethod
    async def set_property(cls, user_id: int, property: Literal["premium", "banned"], value: bool) -> None:
        """Updates an user's property (premium or banned)"""
        await cls.collection.find_one_and_update({"id": str(user_id)}, {"$set": {property: value}})
        return