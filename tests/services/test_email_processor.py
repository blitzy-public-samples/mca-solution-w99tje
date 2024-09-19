import pytest
from unittest.mock import Mock, patch
from src.services.email_processor import EmailProcessor
from src.services.document_classifier import DocumentClassifier
from src.core.config import settings
from src.api.models.application import Application
from src.api.models.document import Document

@pytest.mark.asyncio
async def test_email_processor_initialization():
    # Mock the IMAP4_SSL class
    with patch('imaplib.IMAP4_SSL') as mock_imap:
        # Create an instance of EmailProcessor
        email_processor = EmailProcessor()
        
        # Assert that the IMAP4_SSL constructor was called with correct parameters
        mock_imap.assert_called_once_with(settings.EMAIL_SERVER, settings.EMAIL_PORT)
        
        # Assert that the login method was called with correct credentials
        mock_imap.return_value.login.assert_called_once_with(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        
        # Assert that DocumentClassifier was initialized
        assert isinstance(email_processor.document_classifier, DocumentClassifier)

@pytest.mark.asyncio
async def test_process_emails():
    # Mock the IMAP4_SSL class and its methods
    with patch('imaplib.IMAP4_SSL') as mock_imap, \
         patch('src.services.email_processor.SessionLocal') as mock_session_local, \
         patch('src.services.email_processor.EmailProcessor.parse_email') as mock_parse_email, \
         patch('src.services.email_processor.EmailProcessor.save_attachment') as mock_save_attachment:
        
        # Mock the SessionLocal to return a mock database session
        mock_db = Mock()
        mock_session_local.return_value.__enter__.return_value = mock_db
        
        # Create mock email data
        mock_email_data = {
            'subject': 'Test Subject',
            'sender': 'test@example.com',
            'body': 'Test Body',
            'attachments': [('attachment1.pdf', b'test_content')]
        }
        
        # Mock the parse_email method to return the mock email data
        mock_parse_email.return_value = mock_email_data
        
        # Mock the save_attachment method
        mock_save_attachment.return_value = {'filename': 'attachment1.pdf', 'file_path': '/path/to/attachment1.pdf', 'document_type': 'application_form'}
        
        # Create an instance of EmailProcessor
        email_processor = EmailProcessor()
        
        # Call the process_emails method
        processed_emails = await email_processor.process_emails()
        
        # Assert that the correct IMAP methods were called
        mock_imap.return_value.select.assert_called_once_with('INBOX')
        mock_imap.return_value.search.assert_called_once_with(None, 'ALL')
        mock_imap.return_value.fetch.assert_called()
        
        # Assert that parse_email and save_attachment were called correct number of times
        assert mock_parse_email.call_count == mock_imap.return_value.fetch.return_value[1].__len__.return_value
        assert mock_save_attachment.call_count == len(mock_email_data['attachments'])
        
        # Assert that Application and Document objects were created and added to the session
        mock_db.add.assert_called()
        assert isinstance(mock_db.add.call_args[0][0], Application)
        assert isinstance(mock_db.add.call_args[0][1], Document)
        
        # Assert that the processed email data is returned correctly
        assert len(processed_emails) == mock_imap.return_value.fetch.return_value[1].__len__.return_value
        assert processed_emails[0] == {**mock_email_data, 'attachments': [mock_save_attachment.return_value]}

def test_parse_email():
    # Create a mock email message
    mock_message = Mock()
    mock_message.get.side_effect = lambda x: {'Subject': 'Test Subject', 'From': 'test@example.com'}[x]
    mock_message.get_payload.return_value = 'Test Body'
    mock_attachment = Mock()
    mock_attachment.get_filename.return_value = 'attachment1.pdf'
    mock_attachment.get_payload.return_value = b'test_content'
    mock_message.walk.return_value = [mock_message, mock_attachment]
    
    # Create an instance of EmailProcessor
    email_processor = EmailProcessor()
    
    # Call the parse_email method with the mock message
    parsed_email = email_processor.parse_email(mock_message)
    
    # Assert that the returned data contains the correct subject, sender, body, and attachments
    assert parsed_email['subject'] == 'Test Subject'
    assert parsed_email['sender'] == 'test@example.com'
    assert parsed_email['body'] == 'Test Body'
    assert parsed_email['attachments'] == [('attachment1.pdf', b'test_content')]

def test_save_attachment():
    # Mock the open function
    with patch('builtins.open', Mock()) as mock_open, \
         patch('src.services.document_classifier.DocumentClassifier.classify_document') as mock_classify:
        
        # Mock the DocumentClassifier.classify_document method
        mock_classify.return_value = 'application_form'
        
        # Create a mock attachment
        mock_attachment = ('test_attachment.pdf', b'test_content')
        
        # Create an instance of EmailProcessor
        email_processor = EmailProcessor()
        
        # Call the save_attachment method with the mock attachment
        result = email_processor.save_attachment(mock_attachment)
        
        # Assert that the file was saved correctly
        mock_open.assert_called_once_with(f"{settings.UPLOAD_FOLDER}/test_attachment.pdf", 'wb')
        mock_open.return_value.__enter__.return_value.write.assert_called_once_with(b'test_content')
        
        # Assert that the DocumentClassifier was called
        mock_classify.assert_called_once_with(f"{settings.UPLOAD_FOLDER}/test_attachment.pdf")
        
        # Assert that the returned data contains the correct filename, file path, and document type
        assert result == {
            'filename': 'test_attachment.pdf',
            'file_path': f"{settings.UPLOAD_FOLDER}/test_attachment.pdf",
            'document_type': 'application_form'
        }