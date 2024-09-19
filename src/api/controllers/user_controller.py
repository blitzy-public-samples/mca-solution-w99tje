from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from src.api.models.user import User
from src.api.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from src.core.database import get_db
from src.core.security import get_current_user, get_password_hash, verify_password
from src.utils.logger import logger

router = APIRouter()

@router.post('/', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can create new users")
    
    # Check if user with given email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Create hashed password
    hashed_password = get_password_hash(user.password)
    
    # Create new User instance
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_admin=user.is_admin
    )
    
    # Add user to database session
    db.add(new_user)
    
    # Commit changes to database
    db.commit()
    db.refresh(new_user)
    
    # Log user creation
    logger.info(f"New user created: {new_user.email}")
    
    # Return created user
    return new_user

@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges or is requesting their own information
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's information")
    
    # Query database for user with given ID
    user = db.query(User).filter(User.id == user_id).first()
    
    # If user not found, raise HTTPException
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return found user
    return user

@router.get('/', response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can retrieve user list")
    
    # Query database for users with pagination
    users = db.query(User).offset(skip).limit(limit).all()
    
    # Return list of users
    return users

@router.patch('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges or is updating their own information
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user's information")
    
    # Query database for user with given ID
    user = db.query(User).filter(User.id == user_id).first()
    
    # If user not found, raise HTTPException
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user information
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == 'password':
            # If password is being updated, create new hashed password
            setattr(user, 'hashed_password', get_password_hash(value))
        else:
            setattr(user, field, value)
    
    # Commit changes to database
    db.commit()
    db.refresh(user)
    
    # Log user update
    logger.info(f"User updated: {user.email}")
    
    # Return updated user
    return user

@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete users")
    
    # Query database for user with given ID
    user = db.query(User).filter(User.id == user_id).first()
    
    # If user not found, raise HTTPException
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user from database
    db.delete(user)
    
    # Commit changes to database
    db.commit()
    
    # Log user deletion
    logger.info(f"User deleted: {user.email}")
    
    # Return confirmation message
    return {"message": "User successfully deleted"}