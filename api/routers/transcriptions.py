from fastapi import APIRouter, Request, Depends, UploadFile, File
from ..dependencies import auth, rate_limit
from ..utils import AIModel
from ..database import LogManager

router = APIRouter()

@router.post("/v1/audio/transcriptions", dependencies=[Depends(auth), Depends(rate_limit)], response_model=None)
async def transcriptions(request: Request, file: UploadFile = File(...)) -> dict:
    """Transcriptions endpoint request handler"""

    result = await (AIModel.get_provider("whisper-1"))(await file.read())

    if not isinstance(result, tuple) or len(result) != 2:
        return result

    await LogManager.log_api_request(result[1], "whisper-1", request)

    return result[0]