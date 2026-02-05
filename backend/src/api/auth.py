from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from ..database.session import get_session
from ..models.user_task_models import User
from ..schemas.task_schemas import TaskDetailResponse

# Configuration
import os
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Use SECRET_KEY environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing with fallback schemes
pwd_context = CryptContext(schemes=["bcrypt", "argon2", "plaintext"], deprecated="auto")

# JWT utilities
def verify_password(plain_password, hashed_password):
    # Bcrypt has a 72-byte password length limit, so we truncate if needed
    truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
    return pwd_context.verify(truncated_password, hashed_password)

def get_password_hash(password):
    # Bcrypt has a 72-byte password length limit, so we truncate if needed
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Convert string user ID to integer
        user_id = int(user_id_str)
        return user_id
    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Request/Response models
class UserRegister(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

class AuthResponse(BaseModel):
    success: bool
    data: dict
    message: Optional[str] = None

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=AuthResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = db.execute(select(User).where(User.email == user_data.email)).scalar()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create new user
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return AuthResponse(
        success=True,
        data={
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        },
        message="User registered successfully"
    )


@router.post("/login", response_model=AuthResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_session)):
    # Find user by email
    user = db.execute(select(User).where(User.email == user_data.email)).scalar()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return AuthResponse(
        success=True,
        data={
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        },
        message="Login successful"
    )


@router.post("/logout", response_model=AuthResponse)
async def logout():
    # In a real implementation, you might add the token to a blacklist
    return AuthResponse(
        success=True,
        data={"message": "Logged out successfully"},
        message="Successfully logged out"
    )