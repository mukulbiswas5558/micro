from datetime import datetime, timedelta
import jwt  # Using pyjwt library to handle JWT
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from .config import SECRET_KEY, ALGORITHM
from ..services.user_service import get_user_from_db  # Function to fetch user from the database
# ALGORITHM = "HS256"  # Common and supported algorithm
# SECRET_KEY = "your_secure_key"
print(SECRET_KEY, ALGORITHM)
print("hello")
# OAuth2PasswordBearer provides a way to retrieve the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# CryptContext is used to hash and verify passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token expiration and algorithm settings
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token validity period in minutes

# Define a Pydantic model for the token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Define a Pydantic model for the user data in the token
class User(BaseModel):
    username: str
    role: str  # Role for role-based access

# This function generates a JWT token with an expiration time
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # Adding the expiration to the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Using pyjwt.encode to create the token
    return encoded_jwt

# This function decodes the JWT token to extract the payload
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Using pyjwt.decode to decode the token
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# This function hashes a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# This function verifies a plain password against the hashed password in the database
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# This function extracts the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    username: str = payload.get("sub")  # 'sub' is used for storing the username
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_from_db(username)  # Fetch user from the database by username
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(username=user["username"], role=user["role"])

# Function to check if the current user has admin access
async def check_admin_access(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

# Function to validate token and get the user's role
async def get_current_user_role(token: str = Depends(oauth2_scheme)) -> str:
    payload = decode_access_token(token)
    role: str = payload.get("role")  # Extract the role from the token payload
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate role",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return role
