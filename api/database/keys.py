import yaml
import motor.motor_asyncio as motor

with open("values/secrets.yaml", "r") as f:
    config = yaml.safe_load(f)["db"]

class KeyManager:
    """
    Class for retrieving provider keys from the MongoDB database
    """
    
    _collection = motor.AsyncIOMotorClient(config["mongo_uri"])["db"]["keys"]
    _key_index = {}

    @classmethod
    async def get_valid_key(cls, key_type: str) -> str:
        """Returns a valid key for a given key type using round-robin load balancing"""
        keys = (await cls._collection.find_one({"name": key_type}))["keys"]
        chosen_key = keys[cls._key_index.get(key_type, 0)]
        cls._key_index[key_type] = (cls._key_index.get(key_type, 0) + 1) % len(keys)
        return chosen_key