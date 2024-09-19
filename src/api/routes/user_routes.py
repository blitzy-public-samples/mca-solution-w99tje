from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.api.controllers.user_controller import create_user, get_user, get_users, update_user, delete_user
from src.api.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from src.core.database import get_db
from src.core.security import get_current_user
from src.api.models.user import User

router = APIRouter()

@router.post('/', response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create new users")
    
    # Call create_user function from user_controller
    new_user = create_user(db, user)
    
    # Return the created user
    return new_user

@router.get('/{user_id}', response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges or is requesting their own information
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    # Call get_user function from user_controller
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Return the retrieved user
    return user

@router.get('/', response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can list all users")
    
    # Call get_users function from user_controller
    users = get_users(db, skip=skip, limit=limit)
    
    # Return the list of users
    return users

@router.patch('/{user_id}', response_model=UserResponse)
def update_existing_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges or is updating their own information
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    # Call update_user function from user_controller
    updated_user = update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Return the updated user
    return updated_user

@router.delete('/{user_id}')
def delete_existing_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if current user has admin privileges
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete users")
    
    # Call delete_user function from user_controller
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Return confirmation message
    return {"message": "User deleted successfully"}