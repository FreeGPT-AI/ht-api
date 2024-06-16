import ujson
import yaml
from fastapi import APIRouter, Request, Response
from typing import Union
from ..utils import make_error_response
from ..models import AdminBody
from ..database import UserManager

router = APIRouter()

with open("values/secrets.yml", "r") as f:
    config = yaml.safe_load(f)["api"]

@router.post("/admin", include_in_schema=False, response_model=None)
async def admin(request: Request, data: AdminBody) -> Union[Response, dict]:
    """Admin endpoint request handler"""
    
    auth_key = request.headers.get("Authorization", "").replace("Bearer ", "", 1)

    if auth_key != config["admin_key"]:
        return make_error_response(
            message="Invalid admin key.",
            type="authentication_error",
            status_code=401
        )

    user_exists = await UserManager.get_user_by_id(data.id)
    
    if data.action == "create" and user_exists:
        return make_error_response(
            message="Key already exists.",
            type="admin_error",
            status_code=400
        )
    if data.action in ["get", "update", "delete"] and not user_exists:
        return make_error_response(
            message="Key doesn't exist.",
            type="admin_error",
            status_code=400
        )

    action_map = {
        "create": lambda: UserManager.create_key(data.id),
        "get": lambda: UserManager.get_user_by_id(data.id),
        "delete": lambda: UserManager.delete_key(data.id),
        "update": lambda: UserManager.set_property(data.id, data.property, data.status)
    }

    result = await action_map[data.action]()
    
    if data.action in ["get", "create"]:
        return {"success": True, "value": result}

    return {"success": True, "message": "Successfully executed your action."}