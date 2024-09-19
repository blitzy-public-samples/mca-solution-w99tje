import pytest
from unittest.mock import Mock, patch
from src.services.data_extractor import DataExtractor
from src.services.ocr_engine import OCREngine
from src.api.models.document import DocumentType

def test_data_extractor_initialization():
    # Mock OCREngine
    with patch('src.services.ocr_engine.OCREngine') as mock_ocr_engine:
        # Create an instance of DataExtractor
        data_extractor = DataExtractor()
        
        # Assert that OCREngine was initialized
        mock_ocr_engine.assert_called_once()
        
        # Assert that the instance's ocr_engine attribute is set correctly
        assert isinstance(data_extractor.ocr_engine, Mock)

@pytest.mark.asyncio
async def test_extract_data():
    # Mock OCREngine.perform_ocr to return sample OCR results
    sample_ocr_results = "Sample OCR text"
    with patch('src.services.ocr_engine.OCREngine.perform_ocr', return_value=sample_ocr_results):
        # Create an instance of DataExtractor
        data_extractor = DataExtractor()
        
        # Call extract_data with a mock file path and document type
        file_path = "path/to/document.pdf"
        document_type = DocumentType.BANK_STATEMENT
        result = await data_extractor.extract_data(file_path, document_type)
        
        # Assert that OCREngine.perform_ocr was called with the correct file path
        data_extractor.ocr_engine.perform_ocr.assert_called_once_with(file_path)
        
        # Assert that the appropriate extraction method was called based on the document type
        # This assertion depends on the implementation of extract_data method
        # You may need to adjust this based on your actual implementation
        assert isinstance(result, dict)
        assert "account_holder" in result
        assert "account_number" in result
        # Add more assertions for other expected keys in the result

def test_extract_bank_statement():
    # Create sample OCR results for a bank statement
    sample_ocr_results = """
    Account Holder: John Doe
    Account Number: 1234567890
    Statement Period: 01/01/2023 - 31/01/2023
    Opening Balance: $1000.00
    Closing Balance: $1500.00
    Transactions:
    01/05/2023 Deposit $500.00
    01/15/2023 Withdrawal $200.00
    01/25/2023 Deposit $200.00
    """
    
    # Create an instance of DataExtractor
    data_extractor = DataExtractor()
    
    # Call extract_bank_statement with the sample OCR results
    result = data_extractor.extract_bank_statement(sample_ocr_results)
    
    # Assert that the returned data contains expected keys
    expected_keys = ["account_holder", "account_number", "statement_period", "opening_balance", "closing_balance", "transactions"]
    for key in expected_keys:
        assert key in result
    
    # Verify that the extracted data matches the expected values from the sample OCR results
    assert result["account_holder"] == "John Doe"
    assert result["account_number"] == "1234567890"
    assert result["statement_period"] == "01/01/2023 - 31/01/2023"
    assert result["opening_balance"] == "$1000.00"
    assert result["closing_balance"] == "$1500.00"
    assert len(result["transactions"]) == 3

def test_extract_tax_return():
    # Create sample OCR results for a tax return
    sample_ocr_results = """
    Taxpayer Name: Jane Smith
    Tax Year: 2022
    Total Income: $75,000
    Taxable Income: $60,000
    Tax Paid: $12,000
    """
    
    # Create an instance of DataExtractor
    data_extractor = DataExtractor()
    
    # Call extract_tax_return with the sample OCR results
    result = data_extractor.extract_tax_return(sample_ocr_results)
    
    # Assert that the returned data contains expected keys
    expected_keys = ["taxpayer_name", "tax_year", "total_income", "taxable_income", "tax_paid"]
    for key in expected_keys:
        assert key in result
    
    # Verify that the extracted data matches the expected values from the sample OCR results
    assert result["taxpayer_name"] == "Jane Smith"
    assert result["tax_year"] == "2022"
    assert result["total_income"] == "$75,000"
    assert result["taxable_income"] == "$60,000"
    assert result["tax_paid"] == "$12,000"

def test_extract_business_license():
    # Create sample OCR results for a business license
    sample_ocr_results = """
    Business Name: Acme Corporation
    License Number: BL-12345
    Issue Date: 01/01/2023
    Expiration Date: 12/31/2023
    Business Type: Limited Liability Company
    Business Address: 123 Main St, Anytown, USA 12345
    """
    
    # Create an instance of DataExtractor
    data_extractor = DataExtractor()
    
    # Call extract_business_license with the sample OCR results
    result = data_extractor.extract_business_license(sample_ocr_results)
    
    # Assert that the returned data contains expected keys
    expected_keys = ["business_name", "license_number", "issue_date", "expiration_date", "business_type", "business_address"]
    for key in expected_keys:
        assert key in result
    
    # Verify that the extracted data matches the expected values from the sample OCR results
    assert result["business_name"] == "Acme Corporation"
    assert result["license_number"] == "BL-12345"
    assert result["issue_date"] == "01/01/2023"
    assert result["expiration_date"] == "12/31/2023"
    assert result["business_type"] == "Limited Liability Company"
    assert result["business_address"] == "123 Main St, Anytown, USA 12345"

def test_extract_financial_statement():
    # Create sample OCR results for a financial statement
    sample_ocr_results = """
    Company Name: XYZ Inc.
    Statement Period: Q4 2022
    Revenue: $1,000,000
    Expenses: $800,000
    Net Income: $200,000
    Assets: $5,000,000
    Liabilities: $2,000,000
    Equity: $3,000,000
    """
    
    # Create an instance of DataExtractor
    data_extractor = DataExtractor()
    
    # Call extract_financial_statement with the sample OCR results
    result = data_extractor.extract_financial_statement(sample_ocr_results)
    
    # Assert that the returned data contains expected keys
    expected_keys = ["company_name", "statement_period", "revenue", "expenses", "net_income", "assets", "liabilities", "equity"]
    for key in expected_keys:
        assert key in result
    
    # Verify that the extracted data matches the expected values from the sample OCR results
    assert result["company_name"] == "XYZ Inc."
    assert result["statement_period"] == "Q4 2022"
    assert result["revenue"] == "$1,000,000"
    assert result["expenses"] == "$800,000"
    assert result["net_income"] == "$200,000"
    assert result["assets"] == "$5,000,000"
    assert result["liabilities"] == "$2,000,000"
    assert result["equity"] == "$3,000,000"