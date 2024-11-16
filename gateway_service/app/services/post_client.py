from dotenv import load_dotenv
import os
import httpx

load_dotenv()

# Get the POST_SERVICE_URL from environment variables
POST_SERVICE_URL = os.getenv("POST_SERVICE_URL")
    
async def get_post_data(post_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{POST_SERVICE_URL}/posts/{post_id}")
            if response.status_code == 200:
                return response.json()
            return None
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return None