from fastapi import Request
from ..providers import OpenAI
from ..database import UserManager
from ..exceptions import InvalidRequestException

async def moderation(request: Request) -> None:
    """Moderation dependency (executes before the route handler)"""

    key = request.headers.get("Authorization", "").replace("Bearer ", "", 1)
    is_premium = await UserManager.get_property(key, "premium")
    body = await request.json()

    if not is_premium or any(value in body.get("model", "") for value in ["claude", "dall"]):
        prompt = "\n".join([message.get("content") for message in body.get("messages")]) if body.get("messages") else body.get("prompt")
            
        if not prompt:
            raise InvalidRequestException("You need to provide a valid prompt for moderation.", status=400)
                
        _, client = await OpenAI._get_client()
        result = await client.moderations.create(input=prompt, model="text-moderation-latest")

        if result.results[0].flagged:
            raise InvalidRequestException("No RP for you here, bitch. Buy premium or cope.", status=403)