from fastapi import APIRouter, Request, Response, Depends, UploadFile, File
from typing import Union
from ..dependencies import auth, rate_limit
from ..utils import AIModel
from ..database import LogManager

router = APIRouter()

@router.post("/v1/audio/transcriptions", dependencies=[Depends(auth), Depends(rate_limit)], response_model=None)
async def transcriptions(request: Request, file: UploadFile = File(...)) -> Union[Response, dict]:
    """Transcriptions endpoint request handler"""

    result = await AIModel.get_provider("whisper-1")(await file.read())
    success, log_data = (True, result[1]) if isinstance(result, tuple) and len(result) == 2 else (result[2], result[1])
    
    await LogManager.log_api_request("whisper-1", request, success, key=log_data if success else None, error=log_data if not success else None)
    
    return result[0] if success else result