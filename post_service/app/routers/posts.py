from fastapi import APIRouter, HTTPException
from ..models import Post

router = APIRouter()

fake_posts_db = {
    1: {"id": 1, "title": "First Post", "content": "Content of the first post"},
    2: {"id": 2, "title": "Second Post", "content": "Content of the second post"}
}

@router.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    post = fake_posts_db.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
