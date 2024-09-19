import boto3
from typing import Dict, Any, List
from pathlib import Path
from src.core.config import settings
from src.utils.logger import logger

class OCREngine:
    """Class for performing Optical Character Recognition (OCR) on documents"""

    def __init__(self):
        """Initialize the OCREngine"""
        # Initialize AWS Textract client using boto3
        self.textract_client = boto3.client('textract', 
                                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                            region_name=settings.AWS_REGION)

    def perform_ocr(self, file_path: Path) -> Dict[str, Any]:
        """Perform OCR on a document file"""
        # Read the document file
        with open(file_path, 'rb') as document:
            file_bytes = document.read()

        # Send the document to AWS Textract for processing
        response = self.textract_client.analyze_document(
            Document={'Bytes': file_bytes},
            FeatureTypes=['FORMS', 'TABLES']
        )

        # Receive and parse the OCR results
        ocr_results = {
            'full_text': self.extract_text(response),
            'form_data': self.extract_form_data(response),
            'tables': self.extract_tables(response)
        }

        # Log the OCR process completion
        logger.info(f"OCR completed for file: {file_path}")

        # Return the OCR results
        return ocr_results

    def extract_text(self, textract_result: Dict[str, Any]) -> str:
        """Extract full text from Textract results"""
        # Iterate through Textract blocks
        full_text = []
        for item in textract_result['Blocks']:
            # Collect and concatenate text from relevant blocks
            if item['BlockType'] == 'LINE':
                full_text.append(item['Text'])

        # Return the full extracted text
        return ' '.join(full_text)

    def extract_form_data(self, textract_result: Dict[str, Any]) -> Dict[str, str]:
        """Extract structured form data from Textract results"""
        # Iterate through Textract blocks
        form_data = {}
        key_map = {}
        value_map = {}
        
        for item in textract_result['Blocks']:
            if item['BlockType'] == 'KEY_VALUE_SET':
                if 'KEY' in item['EntityTypes']:
                    key_map[item['Id']] = item
                elif 'VALUE' in item['EntityTypes']:
                    value_map[item['Id']] = item

        # Identify form fields and their corresponding values
        for key_id, key_item in key_map.items():
            value_id = key_item['Relationships'][0]['Ids'][0]
            key_text = key_item['Text']
            value_text = value_map[value_id]['Text'] if value_id in value_map else ''
            
            # Create a dictionary of key-value pairs
            form_data[key_text] = value_text

        # Return the structured form data
        return form_data

    def extract_tables(self, textract_result: Dict[str, Any]) -> List[List[str]]:
        """Extract table data from Textract results"""
        # Iterate through Textract blocks
        tables = []
        table = []
        row = []

        for item in textract_result['Blocks']:
            if item['BlockType'] == 'TABLE':
                table = []
            elif item['BlockType'] == 'CELL':
                if item['RowIndex'] == 1 and item['ColumnIndex'] == 1:
                    if table:
                        tables.append(table)
                    table = []
                if item['ColumnIndex'] == 1:
                    if row:
                        table.append(row)
                    row = []
                row.append(item.get('Text', ''))

        if row:
            table.append(row)
        if table:
            tables.append(table)

        # Return the table data
        return tables