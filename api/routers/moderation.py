from fastapi import APIRouter, Request, Depends, Body
from ..dependencies import auth, rate_limit
from ..typings import ModerationBody
from ..utils import AIModel, InvalidRequestException
from ..database import UserManager, LogManager

router = APIRouter()

@router.post("/v1/moderations", dependencies=[Depends(auth), Depends(rate_limit)])
async def moderation(request: Request, data: ModerationBody = Body(...)) -> dict:
    """Moderation endpoint request handler"""

    key = request.headers.get("Authorization").replace("Bearer ", "", 1)
    premium_check = await UserManager.get_property(key, "premium")
    is_premium_model = data.model in AIModel.get_premium_models("moderations")

    if not premium_check and is_premium_model:
        raise InvalidRequestException("This model is not available in the free tier.", status=402)

    result = await (AIModel.get_provider(data.model))(data.model_dump())

    if not isinstance(result, tuple) or len(result) != 2:
        return result

    await LogManager.log_api_request(result[1], data.model, request)

    return result[0]