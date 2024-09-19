import pytest
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from src.api.controllers.document_controller import upload_document, get_document, get_application_documents
from src.api.models.document import Document
from src.api.models.application import Application
from src.api.models.user import User
from src.services.document_classifier import DocumentClassifier
from src.services.ocr_engine import OCREngine
from src.services.data_extractor import DataExtractor
from src.utils.helpers import save_upload_file

@pytest.mark.asyncio
async def test_upload_document(db_session: Session, mock_user: User, mock_application: Application):
    # Create a mock UploadFile object
    mock_file = UploadFile(filename="test_document.pdf", file=b"test content")

    # Mock the save_upload_file function to return a file path
    mock_file_path = "/tmp/test_document.pdf"
    save_upload_file.return_value = mock_file_path

    # Mock the DocumentClassifier, OCREngine, and DataExtractor services
    mock_classifier = DocumentClassifier()
    mock_classifier.classify.return_value = "ID_PROOF"

    mock_ocr = OCREngine()
    mock_ocr.extract_text.return_value = "Extracted text from document"

    mock_extractor = DataExtractor()
    mock_extractor.extract_data.return_value = {"key": "value"}

    # Call upload_document with the mock file and application ID
    result = await upload_document(db_session, mock_file, mock_application.id, mock_user.id,
                                   mock_classifier, mock_ocr, mock_extractor)

    # Assert that the returned document has the correct attributes
    assert result.filename == "test_document.pdf"
    assert result.file_path == mock_file_path
    assert result.document_type == "ID_PROOF"
    assert result.application_id == mock_application.id
    assert result.uploaded_by == mock_user.id

    # Verify that the document was added to the database session
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()

    # Check that the mocked services were called with the correct arguments
    mock_classifier.classify.assert_called_once_with(mock_file_path)
    mock_ocr.extract_text.assert_called_once_with(mock_file_path)
    mock_extractor.extract_data.assert_called_once_with("Extracted text from document")

@pytest.mark.asyncio
async def test_get_document(db_session: Session, mock_user: User):
    # Create a mock Document object and add it to the database session
    mock_document = Document(id=1, filename="test_document.pdf", file_path="/tmp/test_document.pdf",
                             document_type="ID_PROOF", application_id=1, uploaded_by=mock_user.id)
    db_session.query.return_value.filter.return_value.first.return_value = mock_document

    # Call get_document with the mock document's ID
    result = await get_document(db_session, 1)

    # Assert that the returned document matches the mock document
    assert result == mock_document

    # Test with a non-existent ID and assert that it raises an HTTPException
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        await get_document(db_session, 999)
    assert exc_info.value.status_code == 404
    assert str(exc_info.value.detail) == "Document not found"

@pytest.mark.asyncio
async def test_get_application_documents(db_session: Session, mock_user: User, mock_application: Application):
    # Create multiple mock Document objects associated with the mock application and add them to the database session
    mock_documents = [
        Document(id=1, filename="doc1.pdf", file_path="/tmp/doc1.pdf", document_type="ID_PROOF",
                 application_id=mock_application.id, uploaded_by=mock_user.id),
        Document(id=2, filename="doc2.pdf", file_path="/tmp/doc2.pdf", document_type="INCOME_PROOF",
                 application_id=mock_application.id, uploaded_by=mock_user.id),
    ]
    db_session.query.return_value.filter.return_value.all.return_value = mock_documents

    # Call get_application_documents with the mock application's ID
    result = await get_application_documents(db_session, mock_application.id)

    # Assert that the returned list of documents has the correct length and content
    assert len(result) == 2
    assert result == mock_documents

    # Verify that all returned documents belong to the specified application
    for doc in result:
        assert doc.application_id == mock_application.id

    # Test with a non-existent application ID and assert that it returns an empty list
    db_session.query.return_value.filter.return_value.all.return_value = []
    result = await get_application_documents(db_session, 999)
    assert result == []