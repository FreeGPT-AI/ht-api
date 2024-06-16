from fastapi import APIRouter, Request, Response, Depends, Body
from fastapi.responses import StreamingResponse
from typing import Union
from ..utils import AIModel, InvalidRequestException
from ..models import ChatBody
from ..dependencies import auth, moderation, rate_limit
from ..database import UserManager, LogManager

router = APIRouter()

@router.post("/v1/chat/completions", dependencies=[Depends(auth), Depends(rate_limit), Depends(moderation)], response_model=None)
async def chat(request: Request, data: ChatBody = Body(...)) -> Union[StreamingResponse, Response, dict]:
    """Handle chat completion requests"""

    key = request.headers.get("Authorization").replace("Bearer ", "", 1)
    premium_check = await UserManager.get_property(key, "premium")
    is_premium_model = data.model in AIModel.get_all_models("chat.completions", premium=True)

    if not premium_check and is_premium_model:
        raise InvalidRequestException("This model is not available in the free tier.", status=402)

    result = await AIModel.get_provider(data.model)(data.model_dump())

    if isinstance(result, tuple) and len(result) == 2:
        await LogManager.log_api_request(result[1], data.model, request)
        return result[0]

    return result