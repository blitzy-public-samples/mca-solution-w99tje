import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from src.services.document_classifier import DocumentClassifier
from src.api.models.document import DocumentType

def test_document_classifier_initialization():
    # Create an instance of DocumentClassifier
    classifier = DocumentClassifier()
    
    # Assert that the instance is not None
    assert classifier is not None
    
    # Assert that the instance is of type DocumentClassifier
    assert isinstance(classifier, DocumentClassifier)

def test_classify_document():
    # Mock the extract_text method to return a sample text
    with patch.object(DocumentClassifier, 'extract_text', return_value='Sample document text'):
        # Mock the analyze_metadata method to return sample metadata
        with patch.object(DocumentClassifier, 'analyze_metadata', return_value={'file_size': 1024, 'creation_date': '2023-05-01'}):
            # Create an instance of DocumentClassifier
            classifier = DocumentClassifier()
            
            # Call classify_document with a mock file path and metadata
            mock_file_path = Path('/path/to/mock/document.pdf')
            mock_metadata = {'file_size': 1024, 'creation_date': '2023-05-01'}
            result = classifier.classify_document(mock_file_path, mock_metadata)
            
            # Assert that extract_text and analyze_metadata were called
            classifier.extract_text.assert_called_once_with(mock_file_path)
            classifier.analyze_metadata.assert_called_once_with(mock_metadata)
            
            # Assert that the returned document type is valid
            assert isinstance(result, DocumentType)
            
            # Test with different sample texts and metadata to ensure correct classification
            classifier.extract_text.return_value = 'This is an application form'
            result = classifier.classify_document(mock_file_path, mock_metadata)
            assert result == DocumentType.APPLICATION_FORM
            
            classifier.extract_text.return_value = 'Bank statement for account 12345'
            result = classifier.classify_document(mock_file_path, mock_metadata)
            assert result == DocumentType.BANK_STATEMENT

def test_extract_text():
    # Mock the open function to return a file-like object with sample content
    mock_content = 'This is a sample document content'
    mock_file = Mock()
    mock_file.__enter__.return_value.read.return_value = mock_content
    
    with patch('builtins.open', return_value=mock_file):
        # Create an instance of DocumentClassifier
        classifier = DocumentClassifier()
        
        # Call extract_text with a mock file path
        mock_file_path = Path('/path/to/mock/document.txt')
        result = classifier.extract_text(mock_file_path)
        
        # Assert that the returned text matches the expected content
        assert result == mock_content
        
        # Test with different file types to ensure correct text extraction
        for file_type in ['.txt', '.pdf', '.docx']:
            mock_file_path = Path(f'/path/to/mock/document{file_type}')
            result = classifier.extract_text(mock_file_path)
            assert result == mock_content

def test_analyze_metadata():
    # Create sample metadata dictionaries
    metadata1 = {'file_size': 1024, 'creation_date': '2023-05-01', 'author': 'John Doe'}
    metadata2 = {'file_size': 2048, 'creation_date': '2023-05-02', 'pages': 10}
    
    # Create an instance of DocumentClassifier
    classifier = DocumentClassifier()
    
    # Call analyze_metadata with the sample metadata
    result1 = classifier.analyze_metadata(metadata1)
    result2 = classifier.analyze_metadata(metadata2)
    
    # Assert that the returned analyzed features contain expected keys
    assert set(result1.keys()) == {'file_size', 'creation_date', 'author'}
    assert set(result2.keys()) == {'file_size', 'creation_date', 'pages'}
    
    # Assert that the values of the analyzed features are correct based on the input metadata
    assert result1['file_size'] == 1024
    assert result1['creation_date'] == '2023-05-01'
    assert result1['author'] == 'John Doe'
    assert result2['file_size'] == 2048
    assert result2['creation_date'] == '2023-05-02'
    assert result2['pages'] == 10

def test_apply_classification_rules():
    # Create sample text content and metadata features
    text_content1 = 'This is an application form for a loan'
    metadata_features1 = {'file_size': 1024, 'creation_date': '2023-05-01'}
    
    text_content2 = 'Bank statement for account 12345'
    metadata_features2 = {'file_size': 2048, 'creation_date': '2023-05-02'}
    
    # Create an instance of DocumentClassifier
    classifier = DocumentClassifier()
    
    # Call apply_classification_rules with the sample data
    result1 = classifier.apply_classification_rules(text_content1, metadata_features1)
    result2 = classifier.apply_classification_rules(text_content2, metadata_features2)
    
    # Assert that the returned document type is correct based on the input
    assert result1 == DocumentType.APPLICATION_FORM
    assert result2 == DocumentType.BANK_STATEMENT
    
    # Test with various combinations of text content and metadata to cover all classification rules
    result3 = classifier.apply_classification_rules('Proof of income document', {'file_size': 3072})
    assert result3 == DocumentType.PROOF_OF_INCOME
    
    result4 = classifier.apply_classification_rules('Credit report for John Doe', {'file_size': 4096})
    assert result4 == DocumentType.CREDIT_REPORT
    
    result5 = classifier.apply_classification_rules('Unknown document type', {'file_size': 5120})
    assert result5 == DocumentType.UNKNOWN