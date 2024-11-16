from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    username: str
    password: str
    role: str
    status: str
    created_at: str  # Will expect this as a string
    updated_at: str  # Will expect this as a string

    class Config:
        # Automatically convert datetime to string (ISO format)
        anystr_strip_whitespace = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else str(v)
        }
class RegisterUser(BaseModel):
    name: str
    username: str
    password: str
    role: str
class ResponseUser(BaseModel):
    name: str
    username: str
    role: str
class Token(BaseModel):
    access_token: str
    token_type: str
class LoginRequest(BaseModel):
    username: str
    password: str