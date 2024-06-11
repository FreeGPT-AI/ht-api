from fastapi import APIRouter, Request, Depends, Body
from ..dependencies import auth, moderation, rate_limit
from ..typings import ImageBody
from ..utils import AIModel, InvalidRequestException
from ..database import UserManager, LogManager

router = APIRouter()

@router.post("/v1/images/generations", dependencies=[Depends(auth), Depends(rate_limit), Depends(moderation)])
async def images(request: Request, data: ImageBody = Body(...)) -> dict:
    """Image endpoint request handler"""

    key = request.headers.get("Authorization").replace("Bearer ", "", 1)
    premium_check = await UserManager.get_property(key, "premium")
    is_premium_model = data.model in AIModel.get_premium_models("images.generations")

    if not premium_check and is_premium_model:
        raise InvalidRequestException("This model is not available in the free tier.", status=402)

    result = await (AIModel.get_provider(data.model))(data.model_dump())

    if not isinstance(result, tuple) or len(result) != 2:
        return result

    await LogManager.log_api_request(result[1], data.model, request)

    return result[0]