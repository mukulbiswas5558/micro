from fastapi import FastAPI
from .routers import users


app = FastAPI()

# Include the user router
app.include_router(users.router)
