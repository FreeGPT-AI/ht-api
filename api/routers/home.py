from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home() -> dict:
    """Home endpoint request handler"""
    return {"message": "Welcome to the HentAI API! Join our Discord server: https://discord.gg/8nznYcHqEa"}