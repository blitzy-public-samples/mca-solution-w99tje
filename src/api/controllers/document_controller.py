from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from src.api.models.document import Document
from src.api.schemas.document_schema import DocumentCreate, DocumentUpdate, DocumentResponse
from src.core.database import get_db
from src.core.security import get_current_user
from src.services.document_classifier import DocumentClassifier
from src.services.ocr_engine import OCREngine
from src.services.data_extractor import DataExtractor
from src.utils.helpers import save_upload_file

router = APIRouter()

@router.post('/', response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a new document for an MCA application
    """
    # Save uploaded file using save_upload_file helper
    file_path = await save_upload_file(file)

    # Classify document using DocumentClassifier
    document_classifier = DocumentClassifier()
    document_type = document_classifier.classify(file_path)

    # Perform OCR on document using OCREngine
    ocr_engine = OCREngine()
    ocr_result = ocr_engine.process(file_path)

    # Extract data from OCR result using DataExtractor
    data_extractor = DataExtractor()
    extracted_data = data_extractor.extract(ocr_result)

    # Create new Document instance with extracted data
    new_document = Document(
        application_id=application_id,
        file_path=file_path,
        document_type=document_type,
        extracted_data=extracted_data
    )

    # Add document to database session
    db.add(new_document)

    # Commit changes to database
    db.commit()
    db.refresh(new_document)

    # Return created document
    return new_document

@router.get('/{document_id}', response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific document by ID
    """
    # Query database for document with given ID
    document = db.query(Document).filter(Document.id == document_id).first()

    # If document not found, raise HTTPException
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Return found document
    return document

@router.get('/application/{application_id}', response_model=List[DocumentResponse])
def get_application_documents(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all documents for a specific MCA application
    """
    # Query database for documents associated with given application ID
    documents = db.query(Document).filter(Document.application_id == application_id).all()

    # Return list of documents
    return documents

@router.patch('/{document_id}', response_model=DocumentResponse)
def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing document's metadata
    """
    # Query database for document with given ID
    document = db.query(Document).filter(Document.id == document_id).first()

    # If document not found, raise HTTPException
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Update document with new metadata
    for key, value in document_update.dict(exclude_unset=True).items():
        setattr(document, key, value)

    # Commit changes to database
    db.commit()
    db.refresh(document)

    # Return updated document
    return document