import ujson
import yaml
from fastapi import APIRouter, Request, Response
from typing import Union
from ..typings import AdminBody
from ..database import UserManager

router = APIRouter()

with open("values/secrets.yaml", "rb") as f:
    config = yaml.load(f)["api"]

@router.post("/admin", include_in_schema=False, response_model=None)
async def admin(request: Request, data: AdminBody) -> Union[Response, dict]:
    """Admin endpoint request handler"""

    if request.headers.get("Authorization", "").replace("Bearer ", "", 1) != config["admin_key"]:
        return Response(content=ujson.dumps({"error": "Invalid admin key.", "success": False}, indent=4), status_code=401)
    
    user_exists = await UserManager.get_user_by_id(data.id)
    
    if data.action == "create" and user_exists:
        return Response(content=ujson.dumps({"success": False, "value": "Key already exists."}, indent=4), status_code=400)
    elif data.action in ["get", "update", "delete"] and not user_exists:
        return Response(content=ujson.dumps({"success": False, "value": "Key doesn't exist."}, indent=4), status_code=404)

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