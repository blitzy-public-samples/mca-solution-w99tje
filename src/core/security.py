from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.database import get_db
from src.api.models.user import User

# Create a password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Create an OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/token')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    # Use pwd_context to verify the plain password against the hashed password
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hash for a password
    """
    # Use pwd_context to hash the provided password
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """
    Create a new access token
    """
    # Create a copy of the input data
    to_encode = data.copy()
    
    # Set the expiration time for the token
    expire = datetime.utcnow() + expires_delta
    
    # Add the expiration time to the token data
    to_encode.update({"exp": expire})
    
    # Encode the token data using JWT
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Return the encoded token
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get the current authenticated user
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Extract the user ID from the token payload
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    # Query the database for the user
    user = db.query(User).filter(User.id == user_id).first()
    
    # If user not found, raise HTTPException
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    # Return the user
    return user