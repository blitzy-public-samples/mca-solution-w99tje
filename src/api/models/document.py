from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from src.core.database import Base

# Define the DocumentType enum
DocumentType = Enum('BANK_STATEMENT', 'TAX_RETURN', 'BUSINESS_LICENSE', 'FINANCIAL_STATEMENT', 'OTHER', name='document_type')

class Document(Base):
    """Represents a document associated with an MCA application"""

    __tablename__ = 'documents'

    # Define the columns for the Document table
    id = Column(String, primary_key=True)
    application_id = Column(String, ForeignKey('applications.id'), nullable=False)
    type = Column(DocumentType, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False)
    content_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    md5_hash = Column(String, nullable=False)

    # Define the relationship with the Application model
    application = relationship('Application', back_populates='documents')

    def __init__(self, application_id, type, file_name, file_path, content_type, file_size, md5_hash):
        """
        Initializes a new Document instance

        Args:
            application_id (str): The ID of the associated application
            type (DocumentType): The type of the document
            file_name (str): The name of the file
            file_path (str): The path where the file is stored
            content_type (str): The MIME type of the file
            file_size (int): The size of the file in bytes
            md5_hash (str): The MD5 hash of the file
        """
        # Generate a new UUID for the document
        self.id = str(uuid4())

        # Set the upload_date to the current datetime
        self.upload_date = datetime.utcnow()

        # Assign all provided parameters to the corresponding attributes
        self.application_id = application_id
        self.type = type
        self.file_name = file_name
        self.file_path = file_path
        self.content_type = content_type
        self.file_size = file_size
        self.md5_hash = md5_hash