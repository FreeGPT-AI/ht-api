import ujson
from fastapi import Response
from typing import Union

class PrettyJSONResponse(Response):
    """
    Class for easily generating indented JSON responses
    """
    
    media_type = "application/json"

    def render(self, content: Union[dict, list]) -> bytes:
        """Renders the JSON response by turning it into a bytes object"""
        return ujson.dumps(
            content,
            indent=4,
            ensure_ascii=False,
            separators=(",", ": "),
            escape_forward_slashes=False
        ).encode("utf-8")