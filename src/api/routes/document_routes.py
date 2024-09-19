from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from src.api.controllers.document_controller import upload_document, get_document, get_application_documents
from src.api.schemas.document_schema import DocumentResponse
from src.core.database import get_db
from src.core.security import get_current_user
from src.api.models.user import User

# Create an APIRouter instance for document-related routes
router = APIRouter()

@router.post('/', response_model=DocumentResponse)
async def upload_new_document(
    file: UploadFile = File(...),
    application_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DocumentResponse:
    """
    Route to upload a new document for an MCA application
    """
    try:
        # Call upload_document function from document_controller
        uploaded_document = await upload_document(file, application_id, db, current_user)
        
        # Return the uploaded document
        return uploaded_document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/{document_id}', response_model=DocumentResponse)
async def read_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DocumentResponse:
    """
    Route to retrieve a specific document by ID
    """
    try:
        # Call get_document function from document_controller
        document = await get_document(document_id, db, current_user)
        
        # Return the retrieved document
        return document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/application/{application_id}', response_model=List[DocumentResponse])
async def read_application_documents(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[DocumentResponse]:
    """
    Route to retrieve all documents for a specific MCA application
    """
    try:
        # Call get_application_documents function from document_controller
        documents = await get_application_documents(application_id, db, current_user)
        
        # Return the list of documents
        return documents
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))