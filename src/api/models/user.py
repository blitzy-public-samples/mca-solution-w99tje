from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from src.core.database import Base

# Define the UserRole enum
UserRole = Enum('ADMIN', 'MANAGER', 'DATA_ENTRY_SPECIALIST', 'API_USER', name='user_role')

class User(Base):
    """Represents a user in the MCA application processing system"""

    __tablename__ = 'users'

    # Define the columns for the User table
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(UserRole, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __init__(self, email: str, hashed_password: str, full_name: str, role: UserRole):
        """
        Initializes a new User instance
        """
        # Generate a new UUID for the user
        self.id = str(uuid4())
        
        # Set the email, hashed_password, full_name, and role
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.role = role
        
        # Set is_active to True by default
        self.is_active = True
        
        # Set created_at to the current datetime
        self.created_at = datetime.utcnow()
        
        # Initialize last_login as None
        self.last_login = None

    def update_last_login(self):
        """
        Updates the last login timestamp for the user
        """
        # Set the last_login attribute to the current datetime
        self.last_login = datetime.utcnow()