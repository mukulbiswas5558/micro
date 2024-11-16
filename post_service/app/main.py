from fastapi import FastAPI
from .routers import posts
from .database import initialize_db

app = FastAPI()

# Include the post router
app.include_router(posts.router)

@app.on_event("startup")
def startup_event():
    initialize_db()
