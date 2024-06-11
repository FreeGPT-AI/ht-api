import httpx
from typing import Optional
from ...database import KeyManager
from ...utils import handle_errors

class StableDiffusion:
    """
    Default Stable Diffusion provider
    """
    
    @classmethod
    async def upload_image(data: bytes) -> Optional[str]:
        """Uploads a bytes-encoded image to ImgBB"""

        url = "https://api.imgbb.com/1/upload?expiration=60000&key=2a7810f7558ed7c3aa41a8e0f7286e65" # this key is dead, don't even try
        files = {"image": ("image.jpg", data, "image/jpeg")}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, files=files)
            response_data = response.json()

        return response_data.get("data", {}).get("url")

    @classmethod
    @handle_errors
    async def image(cls, body: dict) -> tuple[dict[str, list], str]:
        """Performs an image generation request"""

        key = await KeyManager.get_valid_key("stable-diffusion")
        url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
        headers = {"Authorization": f"Bearer {key}"}
        data = {"prompt": body.get("prompt"), "output_format": "jpeg"}
        
        print(f"[!] Chosen key: {key}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, files={"none": ""}, headers=headers)
            response.raise_for_status()
            uploaded_url = await cls.upload_image(response.content)
        
        return {"data": [{"url": uploaded_url}]}, key
