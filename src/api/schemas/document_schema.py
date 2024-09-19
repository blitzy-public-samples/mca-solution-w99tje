from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from src.api.models.document import DocumentType

class DocumentBase(BaseModel):
    """Base schema for document data"""
    type: DocumentType
    file_name: str
    content_type: str
    file_size: int

class DocumentCreate(DocumentBase):
    """Schema for creating a new document"""
    application_id: UUID

class DocumentUpdate(BaseModel):
    """Schema for updating an existing document"""
    type: Optional[DocumentType] = None
    file_name: Optional[str] = None

class DocumentResponse(DocumentBase):
    """Schema for document response data"""
    id: UUID
    application_id: UUID
    file_path: str
    upload_date: datetime
    md5_hash: str

    class Config:
        orm_mode = True