from fastapi import APIRouter
from ..utils import AIModel

router = APIRouter()

@router.get("/v1/models")
async def models() -> dict:
    """Models endpoint request handler"""
    return AIModel.all_to_json()