from fastapi import Request
from ..providers import OpenAI
from ..database import UserManager
from ..exceptions import InvalidRequestException

async def moderation(request: Request) -> None:
    """Moderation dependency (executes before the route handler)"""

    body = await request.json()
    key = request.headers.get("Authorization", "").replace("Bearer ", "", 1)
    is_premium = await UserManager.get_property(key, "premium")

    if any(value in body.get("model", "") for value in ["claude", "dall"]) or is_premium is False:
        match request.url.path:
            case "/v1/chat/completions":
                prompt = "\n".join([message.get("content", "Hello!") for message in body.get("messages", [{}])])
            case "/v1/images/generations":
                prompt = body.get("prompt", "Cat")
                
        _, client = await OpenAI._get_client()
        result = await client.moderations.create(input=prompt, model="text-moderation-latest")

        if result.results[0].flagged:
            raise InvalidRequestException("No RP for you here, bitch. Buy premium or cope.", status=403)