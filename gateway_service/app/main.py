from fastapi import FastAPI
from .routers import api_gateway

app = FastAPI()

# Include the API gateway router
app.include_router(api_gateway.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)