import os
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from ..models import Key

class KeyManager:
    """
    Class for retrieving provider keys from the MongoDB database
    """
    
    _key_index = {}
    _engine = AIOEngine(
        client=AsyncIOMotorClient(os.environ["MONGO_URI"]),
        database="db"
    )

    @classmethod
    async def get_valid_key(cls, key_type: str) -> str:
        """Returns a valid key for a given key type using round-robin load balancing"""
        keys = await cls._engine.find_one(Key, Key.name == key_type)
        chosen_key = keys.keys[cls._key_index.get(key_type, 0)]
        cls._key_index[key_type] = (cls._key_index.get(key_type, 0) + 1) % len(keys.keys)
        return chosen_key