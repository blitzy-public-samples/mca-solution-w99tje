from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from src.core.database import Base

# Define the WebhookEventType enum
WebhookEventType = Enum('APPLICATION_CREATED', 'APPLICATION_UPDATED', 'DOCUMENT_UPLOADED', 'APPLICATION_APPROVED', 'APPLICATION_REJECTED', name='webhook_event_type')

class Webhook(Base):
    """
    Represents a webhook configuration in the MCA application processing system
    """
    __tablename__ = 'webhooks'

    # Define the columns for the Webhook table
    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    event_type = Column(WebhookEventType, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    last_triggered_at = Column(DateTime)
    retry_count = Column(Integer, default=0)

    def __init__(self, url: str, event_type: WebhookEventType):
        """
        Initializes a new Webhook instance
        """
        # Generate a new UUID for the webhook
        self.id = str(uuid4())
        
        # Set the url and event_type
        self.url = url
        self.event_type = event_type
        
        # Set is_active to True by default
        self.is_active = True
        
        # Set created_at to the current datetime
        self.created_at = datetime.utcnow()
        
        # Initialize last_triggered_at as None
        self.last_triggered_at = None
        
        # Set retry_count to 0
        self.retry_count = 0

    def update_last_triggered(self):
        """
        Updates the last triggered timestamp for the webhook
        """
        # Set the last_triggered_at attribute to the current datetime
        self.last_triggered_at = datetime.utcnow()

    def increment_retry_count(self):
        """
        Increments the retry count for the webhook
        """
        # Increment the retry_count attribute by 1
        self.retry_count += 1