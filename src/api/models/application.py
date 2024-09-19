from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from src.core.database import Base
from src.api.models.document import Document
from src.api.models.merchant import Merchant
from src.api.models.owner import Owner
from src.api.models.funding import Funding

# Define the ApplicationStatus enum
ApplicationStatus = Enum('PENDING', 'APPROVED', 'REJECTED', 'UNDER_REVIEW', name='application_status')

class Application(Base):
    """Represents an MCA application in the system"""

    __tablename__ = 'applications'

    # Define columns
    id = Column(String, primary_key=True)
    email_id = Column(String, nullable=False)
    status = Column(ApplicationStatus, nullable=False)
    received_date = Column(DateTime, nullable=False)
    processed_date = Column(DateTime)

    # Define relationships
    documents = relationship('Document', back_populates='application')
    merchant = relationship('Merchant', back_populates='application', uselist=False)
    owners = relationship('Owner', back_populates='application')
    funding = relationship('Funding', back_populates='application', uselist=False)

    def __init__(self):
        """Initializes a new Application instance"""
        # Generate a new UUID for the application
        self.id = str(uuid4())
        
        # Set the received_date to the current datetime
        self.received_date = datetime.utcnow()
        
        # Set the initial status to PENDING
        self.status = ApplicationStatus.PENDING