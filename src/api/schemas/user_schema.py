from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from src.api.models.user import UserRole

# Base schema for user data
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole

# Schema for creating a new user
class UserCreate(UserBase):
    password: str

# Schema for updating an existing user
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Schema for user response data
class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None