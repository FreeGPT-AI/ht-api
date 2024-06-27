import os
import hashlib
from datetime import datetime, timedelta, timezone
from fastapi import Header
from redis.asyncio import Redis
from ..database import UserManager
from ..exceptions import InvalidRequestException

redis = Redis(
    host=os.environ["REDIS_HOST"].split(":")[0],
    password=os.environ["REDIS_PASSWORD"],
    port=int(os.environ["REDIS_HOST"].split(":")[1]),
    ssl=True
)

async def rate_limit(authorization: str = Header()) -> None:
    """Rate limiting dependency (executes before the route handler)"""

    key = authorization.replace("Bearer ", "", 1)
    is_premium = await UserManager.get_property(key, "premium")

    username_hash = hashlib.sha256(bytes(key, "utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    current_minute = now.strftime("%Y-%m-%dT%H:%M")

    redis_key = f"rate_limit_{username_hash}_{current_minute}"
    current_count = await redis.incr(redis_key)

    if current_count == 1:
        await redis.expireat(name=redis_key, when=now + timedelta(minutes=1))

    if current_count > (10 if is_premium else 3):
        raise InvalidRequestException("Rate limit exceeded.", status=429)