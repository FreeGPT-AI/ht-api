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
    """Chat completions endpoint request handler"""
    
    key = request.headers.get("Authorization").replace("Bearer ", "", 1)
    premium = await UserManager.get_property(key, "premium")
    is_model_premium = data.model in AIModel.get_all_models("chat.completions", premium=True)

    if not premium and is_model_premium:
        raise InvalidRequestException("This model is not available in the free tier.", status=402)
    
    result = await AIModel.get_provider(data.model)(data.model_dump())
    success, log_data = (True, result[1]) if isinstance(result, tuple) and len(result) == 2 else (result[2], result[1])

    await LogManager.log_api_request(data.model, request, success, key=log_data if success else None, error=log_data if not success else None)
    
    return result[0] if success else result