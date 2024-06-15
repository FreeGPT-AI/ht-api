from fastapi import APIRouter, Request, Depends, Body
from ..dependencies import auth, rate_limit
from ..typings import EmbeddingBody
from ..utils import AIModel, InvalidRequestException
from ..database import UserManager, LogManager

router = APIRouter()

@router.post("/v1/embeddings", dependencies=[Depends(auth), Depends(rate_limit)])
async def embedding(request: Request, data: EmbeddingBody = Body(...)) -> dict:
    """Embedding endpoint request handler"""

    key = request.headers.get("Authorization").replace("Bearer ", "", 1)
    premium_check = await UserManager.get_property(key, "premium")
    is_premium_model = data.model in AIModel.get_all_models("embeddings", premium=True)

    if not premium_check and is_premium_model:
        raise InvalidRequestException("This model is not available in the free tier.", status=402)

    result = await AIModel.get_provider(data.model)(data.model_dump())

    if isinstance(result, tuple) and len(result) == 2:
        await LogManager.log_api_request(result[1], data.model, request)
        return result[0]

    return result