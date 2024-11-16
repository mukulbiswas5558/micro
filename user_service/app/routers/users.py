from fastapi import APIRouter, Depends, HTTPException
from ..models.user_model import User, RegisterUser, ResponseUser , LoginRequest, Token
from ..database import get_db
from ..services.user_service import create_user, get_user_from_db, get_username_from_db
from ..utils.auth import create_access_token, verify_password, get_current_user, hash_password

router = APIRouter()

# Register new user
@router.post("/register", response_model=ResponseUser)
async def register_user(user: RegisterUser, db=Depends(get_db)):
    
    # Check if the username already exists
    existing_user = await get_username_from_db(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Modify user data before saving (set default role if not provided)
    modified_user_data = {
        "name": user.name,
        "username": user.username,
        "password": hashed_password,  # Store the hashed password
        "role": user.role or "user",  # Default role to 'user' if not provided
    }

    # Create the new user in the database
    new_user = await create_user(db, **modified_user_data)
    
    # Remove sensitive fields like password from the response
    new_user.pop("password", None)
    return new_user


@router.post("/login", response_model=Token)
async def login_user(login_request: LoginRequest, db=Depends(get_db)):
    """
    Authenticate user and return a JWT token.
    """
    # Extract username and password from the request
    username = login_request.username
    password = login_request.password

    # Fetch user from the database by username
    user = await get_username_from_db(db, username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate a JWT token
    token_data = {"sub": user["username"], "role": user["role"]}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}
# Get user by ID (role-based access control: only admin can access)
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db=Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Get a user by ID with role-based access control (only admin can access).

    Args:
        user_id (int): The ID of the user to retrieve.
        db: The database dependency.
        current_user: The currently authenticated user, used to check permissions.

    Returns:
        dict: The user data, if the current user is authorized to view it.
    """
    # Retrieve user from database
    user = await get_user_from_db(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Role-based access control: only admin can access user data
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return user
