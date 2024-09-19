from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Create a SQLAlchemy engine instance
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a sessionmaker, which will be used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency function to get a database session.

    Returns:
        Generator[Session, None, None]: A database session
    """
    # Create a new SessionLocal instance
    db = SessionLocal()
    try:
        # Yield the session
        yield db
    finally:
        # Ensure the session is closed after use
        db.close()