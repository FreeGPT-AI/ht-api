import base64
import yaml
from httpx import AsyncClient
from typing import Optional
from ...database import KeyManager
from ...utils import handle_errors

with open("values/secrets.yaml", "r") as f:
    keys = yaml.safe_load(f)["keys"]

class StableDiffusion:
    """
    Default Stable Diffusion provider
    """
    
    @staticmethod
    async def _upload_image(data: bytes, client: AsyncClient) -> Optional[str]:
        """Uploads a bytes-encoded image to ImgBB"""

        url = f"https://api.imgbb.com/1/upload?expiration=60000&key={keys['imgbb']}"
        files = {"image": ("image.jpg", data, "image/jpeg")}

        response = await client.post(url, files=files)
        response_data = response.json()
        
        return response_data.get("data", {}).get("url")

    @classmethod
    @handle_errors
    async def image(cls, body: dict) -> tuple[dict[str, list], str]:
        """Performs an image generation request"""

        key = await KeyManager.get_valid_key("stable-diffusion")
        model_endpoint = "v2beta/stable-image/generate/sd3" if body["model"] != "sdxl" else "v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        url = f"https://api.stability.ai/{model_endpoint}"
        headers = {"Authorization": f"Bearer {key}"}
        
        if body["model"] != "sdxl":
            data = {"prompt": body["prompt"], "output_format": "jpeg"}
        else:
            data = {"text_prompts": [{"text": body["prompt"], "weight": 1}]}
        
        async with AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()
            
            if body["model"] != "sdxl":
                uploaded_url = await cls._upload_image(response.content, client)
            else:
                uploaded_url = await cls._upload_image(base64.b64decode(response.json()["artifacts"][0]["base64"]), client)
        
        return {"data": [{"url": uploaded_url}]}, key