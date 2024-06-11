import aiohttp
from ...database import KeyManager
from ...utils import handle_errors

class SDXL:
    """
    Default SDXL provider
    """

    @classmethod
    @handle_errors
    async def image(cls, body: dict) -> tuple[dict[str, list], str]:
        """Performs an image generation request"""
        
        key = await KeyManager.get_valid_key("deepinfra")
        url = "https://api.deepinfra.com/v1/inference/stability-ai/sdxl"
        payload = {"input": {"prompt": body["prompt"]}}
        headers = {"Authorization": f"Bearer {key}"}

        print(f"[!] Chosen key: {key}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()

        return {"data": [{"url": data["output"][0]}]}, key