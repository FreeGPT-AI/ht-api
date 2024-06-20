from fastapi import APIRouter, Request, Response, Depends, Body
from typing import Union
from ..dependencies import auth, moderation, rate_limit
from ..models import ImageBody
from ..utils import AIModel, InvalidRequestException
from ..database import UserManager, LogManager

router = APIRouter()

@router.post("/v1/images/generations", dependencies=[Depends(auth), Depends(rate_limit), Depends(moderation)], response_model=None)
async def images(request: Request, data: ImageBody = Body(...)) -> Union[Response, dict]:
    """Image endpoint request handler"""

    key = request.headers.get("Authorization").replace("Bearer ", "", 1)
    premium = await UserManager.get_property(key, "premium")
    is_model_premium = data.model in AIModel.get_all_models("images.generations", premium=True)

    if not premium and is_model_premium:
        raise InvalidRequestException("This model is not available in the free tier.", status=402)
    
    result = await AIModel.get_provider(data.model)(data.model_dump())
    success, log_data = (True, result[1]) if isinstance(result, tuple) and len(result) == 2 else (result[2], result[1])
    
    await LogManager.log_api_request(data.model, request, success, key=log_data, error=log_data if not success else None)
    
    return result[0] if success else result