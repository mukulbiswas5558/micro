from dotenv import load_dotenv
import os
import httpx

load_dotenv()
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")


async def get_user_data(user_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
            if response.status_code == 200:
                return response.json()
            return None
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return None