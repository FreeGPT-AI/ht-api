import yaml
import aiohttp
from aiocache import cached, Cache
from fastapi import Request
from ..database import UserManager
from ..exceptions import InvalidRequestException

with open("values/secrets.yaml", "rb") as f:
    config = yaml.load(f)["db"]

@cached(cache=Cache.from_url(config["redis_uri"]))
async def check_profanity(body: dict, path: str) -> None:
    """Checks if the request contains profanity"""
    
    match path:
        case "/v1/chat/completions":
            prompt = "\n".join([message.get("content", "Hello!") for message in body.get("messages", [{}])])
            data = {"comment": prompt, "modelName": "PROFANITY", "sessionId": "1290466507630"}
        case "/v1/images/generations":
            data = {"comment": body.get("prompt", "Cat"), "modelName": "PROFANITY", "sessionId": "1290466507630"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url="https://www.perspectiveapi.com/plugin/check", json=data) as response:
                response.raise_for_status()
                result = await response.json()
                if result["attributeScores"]["PROFANITY"]["summaryScore"]["value"] >= 0.7:
                    raise InvalidRequestException("Profanity detected.", status=403)
        except (aiohttp.ClientResponseError, KeyError):
            pass

async def moderation(request: Request) -> None:
    """Moderation dependency (executes before the route handler)"""

    body = await request.json()
    key = request.headers.get("Authorization", "").replace("Bearer ", "", 1)
    is_premium = await UserManager.get_property(key, "premium")

    if ("gpt" not in body.get("model") and isinstance(is_premium, bool)) or not is_premium:
        await check_profanity(body, request.url.path)