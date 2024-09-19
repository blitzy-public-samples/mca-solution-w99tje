import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from src.services.ocr_engine import OCREngine
from src.core.config import settings
import boto3

def test_ocr_engine_initialization():
    # Mock boto3.client
    with patch('boto3.client') as mock_boto3_client:
        # Create an instance of OCREngine
        ocr_engine = OCREngine()
        
        # Assert that boto3.client was called with 'textract' and correct AWS credentials
        mock_boto3_client.assert_called_once_with(
            'textract',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        # Assert that the instance's textract_client attribute is set correctly
        assert ocr_engine.textract_client == mock_boto3_client.return_value

@pytest.mark.asyncio
async def test_perform_ocr():
    # Mock the textract_client.analyze_document method to return sample Textract results
    mock_textract_response = {
        'Blocks': [
            {'BlockType': 'LINE', 'Text': 'Sample text'},
            {'BlockType': 'KEY_VALUE_SET', 'EntityTypes': ['KEY'], 'Text': 'Field'},
            {'BlockType': 'KEY_VALUE_SET', 'EntityTypes': ['VALUE'], 'Text': 'Value'},
            {'BlockType': 'TABLE', 'Relationships': [{'Type': 'CHILD', 'Ids': ['cell1', 'cell2']}]},
        ]
    }
    
    with patch('src.services.ocr_engine.OCREngine.textract_client') as mock_textract_client, \
         patch('builtins.open', mock_open(read_data=b'dummy_file_content')):
        
        mock_textract_client.analyze_document.return_value = mock_textract_response
        
        # Create an instance of OCREngine
        ocr_engine = OCREngine()
        
        # Call perform_ocr with a mock file path
        mock_file_path = Path('/path/to/mock/file.pdf')
        ocr_results = await ocr_engine.perform_ocr(mock_file_path)
        
        # Assert that textract_client.analyze_document was called with correct parameters
        mock_textract_client.analyze_document.assert_called_once_with(
            Document={'Bytes': b'dummy_file_content'},
            FeatureTypes=['TABLES', 'FORMS']
        )
        
        # Assert that the returned OCR results contain expected keys
        assert set(ocr_results.keys()) == {'full_text', 'form_data', 'tables'}
        
        # Verify that extract_text, extract_form_data, and extract_tables methods were called
        assert ocr_results['full_text'] == 'Sample text'
        assert ocr_results['form_data'] == {'Field': 'Value'}
        assert ocr_results['tables'] == [[]]

def test_extract_text():
    # Create sample Textract results with text blocks
    sample_results = {
        'Blocks': [
            {'BlockType': 'LINE', 'Text': 'First line'},
            {'BlockType': 'LINE', 'Text': 'Second line'},
            {'BlockType': 'WORD', 'Text': 'Ignored word'},
        ]
    }
    
    # Create an instance of OCREngine
    ocr_engine = OCREngine()
    
    # Call extract_text with the sample results
    extracted_text = ocr_engine.extract_text(sample_results)
    
    # Assert that the returned text is correctly concatenated from the text blocks
    assert extracted_text == 'First line\nSecond line'

def test_extract_form_data():
    # Create sample Textract results with form fields and values
    sample_results = {
        'Blocks': [
            {'BlockType': 'KEY_VALUE_SET', 'EntityTypes': ['KEY'], 'Relationships': [{'Type': 'VALUE', 'Ids': ['2']}], 'Text': 'Name'},
            {'BlockType': 'KEY_VALUE_SET', 'EntityTypes': ['VALUE'], 'Id': '2', 'Text': 'John Doe'},
            {'BlockType': 'KEY_VALUE_SET', 'EntityTypes': ['KEY'], 'Relationships': [{'Type': 'VALUE', 'Ids': ['4']}], 'Text': 'Age'},
            {'BlockType': 'KEY_VALUE_SET', 'EntityTypes': ['VALUE'], 'Id': '4', 'Text': '30'},
        ]
    }
    
    # Create an instance of OCREngine
    ocr_engine = OCREngine()
    
    # Call extract_form_data with the sample results
    form_data = ocr_engine.extract_form_data(sample_results)
    
    # Assert that the returned dictionary contains correct key-value pairs from the form fields
    assert form_data == {'Name': 'John Doe', 'Age': '30'}

def test_extract_tables():
    # Create sample Textract results with table structures
    sample_results = {
        'Blocks': [
            {'BlockType': 'TABLE', 'Relationships': [{'Type': 'CHILD', 'Ids': ['1', '2', '3', '4']}]},
            {'BlockType': 'CELL', 'Id': '1', 'RowIndex': 1, 'ColumnIndex': 1, 'Text': 'Header 1'},
            {'BlockType': 'CELL', 'Id': '2', 'RowIndex': 1, 'ColumnIndex': 2, 'Text': 'Header 2'},
            {'BlockType': 'CELL', 'Id': '3', 'RowIndex': 2, 'ColumnIndex': 1, 'Text': 'Data 1'},
            {'BlockType': 'CELL', 'Id': '4', 'RowIndex': 2, 'ColumnIndex': 2, 'Text': 'Data 2'},
        ]
    }
    
    # Create an instance of OCREngine
    ocr_engine = OCREngine()
    
    # Call extract_tables with the sample results
    tables = ocr_engine.extract_tables(sample_results)
    
    # Assert that the returned list of tables contains correct data in a 2D list format
    assert tables == [
        [
            ['Header 1', 'Header 2'],
            ['Data 1', 'Data 2']
        ]
    ]