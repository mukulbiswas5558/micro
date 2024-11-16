from fastapi import APIRouter, HTTPException
from ..services.user_client import get_user_data
from ..services.post_client import get_post_data

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await get_user_data(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    post = await get_post_data(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


