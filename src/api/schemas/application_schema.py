from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from src.api.models.application import ApplicationStatus

# Base schema for MCA application data
class ApplicationBase(BaseModel):
    applicant_email: EmailStr
    business_name: str
    business_type: str
    requested_amount: float
    purpose_of_funding: str

# Schema for creating a new MCA application
class ApplicationCreate(ApplicationBase):
    pass

# Schema for updating an existing MCA application
class ApplicationUpdate(ApplicationBase):
    status: Optional[ApplicationStatus] = None

# Schema for MCA application response data
class ApplicationResponse(ApplicationBase):
    id: UUID
    status: ApplicationStatus
    received_date: datetime
    processed_date: Optional[datetime] = None