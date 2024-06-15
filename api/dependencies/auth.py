from fastapi import Request
from ..database import UserManager
from ..exceptions import InvalidRequestException

async def auth(request: Request) -> None:
    """Authentication dependency (executes before the route handler)"""

    auth_header = request.headers.get("Authorization", "")
    key = auth_header.replace("Bearer ", "", 1)

    if not key:
        raise InvalidRequestException("Missing authorization header.", status=401)
    
    if not await UserManager.check_key(key):
        raise InvalidRequestException("Your key is invalid.", status=401)
    
    if await UserManager.get_property(key, "banned"):
        raise InvalidRequestException("Your key is banned.", status=401)