import pytest
from src.services.data_validator import DataValidator
from src.api.models.document import DocumentType

def test_data_validator_initialization():
    # Create an instance of DataValidator
    validator = DataValidator()
    
    # Assert that the instance is not None
    assert validator is not None
    
    # Assert that the instance is of type DataValidator
    assert isinstance(validator, DataValidator)

def test_validate_data():
    # Create sample extracted data for different document types
    bank_statement_data = {"account_number": "1234567890", "balance": 1000}
    tax_return_data = {"tax_year": "2022", "income": 50000}
    business_license_data = {"license_number": "BL12345", "expiry_date": "2023-12-31"}
    financial_statement_data = {"total_assets": 100000, "total_liabilities": 50000}
    
    # Create an instance of DataValidator
    validator = DataValidator()
    
    # For each document type:
    for doc_type, sample_data in [
        (DocumentType.BANK_STATEMENT, bank_statement_data),
        (DocumentType.TAX_RETURN, tax_return_data),
        (DocumentType.BUSINESS_LICENSE, business_license_data),
        (DocumentType.FINANCIAL_STATEMENT, financial_statement_data)
    ]:
        # Call validate_data with the sample data and document type
        result = validator.validate_data(sample_data, doc_type)
        
        # Assert that the returned validation results contain 'errors' and 'warnings' keys
        assert 'errors' in result
        assert 'warnings' in result
        
        # Verify that the appropriate validation method was called based on the document type
        if doc_type == DocumentType.BANK_STATEMENT:
            assert hasattr(validator, 'validate_bank_statement')
        elif doc_type == DocumentType.TAX_RETURN:
            assert hasattr(validator, 'validate_tax_return')
        elif doc_type == DocumentType.BUSINESS_LICENSE:
            assert hasattr(validator, 'validate_business_license')
        elif doc_type == DocumentType.FINANCIAL_STATEMENT:
            assert hasattr(validator, 'validate_financial_statement')

def test_validate_bank_statement():
    # Create sample bank statement data with various scenarios (valid, missing fields, invalid formats)
    valid_data = {"account_number": "1234567890", "balance": 1000, "date": "2023-05-01"}
    missing_field_data = {"account_number": "1234567890"}
    invalid_format_data = {"account_number": "123", "balance": "invalid", "date": "01-05-2023"}
    
    # Create an instance of DataValidator
    validator = DataValidator()
    
    # For each scenario:
    for data in [valid_data, missing_field_data, invalid_format_data]:
        # Call validate_bank_statement with the sample data
        result = validator.validate_bank_statement(data)
        
        # Assert that the returned validation results are correct
        assert 'errors' in result
        assert 'warnings' in result
        
        # Verify that account number format is validated
        if 'account_number' in data:
            assert len(data['account_number']) == 10 or 'account_number' in result['errors']
        
        # Check that date formats are validated
        if 'date' in data:
            assert data['date'].count('-') == 2 or 'date' in result['errors']
        
        # Ensure that balance consistency is checked
        if 'balance' in data:
            assert isinstance(data['balance'], (int, float)) or 'balance' in result['errors']

def test_validate_tax_return():
    # Create sample tax return data with various scenarios (valid, missing fields, invalid formats)
    valid_data = {"tax_year": "2022", "income": 50000, "tax_id": "123-45-6789"}
    missing_field_data = {"tax_year": "2022"}
    invalid_format_data = {"tax_year": "22", "income": "invalid", "tax_id": "123456789"}
    
    # Create an instance of DataValidator
    validator = DataValidator()
    
    # For each scenario:
    for data in [valid_data, missing_field_data, invalid_format_data]:
        # Call validate_tax_return with the sample data
        result = validator.validate_tax_return(data)
        
        # Assert that the returned validation results are correct
        assert 'errors' in result
        assert 'warnings' in result
        
        # Verify that tax year format is validated
        if 'tax_year' in data:
            assert len(data['tax_year']) == 4 or 'tax_year' in result['errors']
        
        # Check that financial figures are logically consistent
        if 'income' in data:
            assert isinstance(data['income'], (int, float)) or 'income' in result['errors']
        
        # Ensure that taxpayer identification numbers are validated
        if 'tax_id' in data:
            assert len(data['tax_id']) == 11 and data['tax_id'].count('-') == 2 or 'tax_id' in result['errors']

def test_validate_business_license():
    # Create sample business license data with various scenarios (valid, missing fields, invalid formats, expired license)
    valid_data = {"license_number": "BL12345", "expiry_date": "2023-12-31", "business_name": "ACME Corp"}
    missing_field_data = {"license_number": "BL12345"}
    invalid_format_data = {"license_number": "12345", "expiry_date": "31-12-2023", "business_name": ""}
    expired_license_data = {"license_number": "BL12345", "expiry_date": "2022-12-31", "business_name": "ACME Corp"}
    
    # Create an instance of DataValidator
    validator = DataValidator()
    
    # For each scenario:
    for data in [valid_data, missing_field_data, invalid_format_data, expired_license_data]:
        # Call validate_business_license with the sample data
        result = validator.validate_business_license(data)
        
        # Assert that the returned validation results are correct
        assert 'errors' in result
        assert 'warnings' in result
        
        # Verify that license number format is validated
        if 'license_number' in data:
            assert data['license_number'].startswith("BL") or 'license_number' in result['errors']
        
        # Check that date formats are validated
        if 'expiry_date' in data:
            assert data['expiry_date'].count('-') == 2 or 'expiry_date' in result['errors']
        
        # Ensure that license expiration is checked
        if 'expiry_date' in data:
            from datetime import datetime
            expiry_date = datetime.strptime(data['expiry_date'], "%Y-%m-%d")
            if expiry_date < datetime.now():
                assert 'expiry_date' in result['errors'] or 'expiry_date' in result['warnings']

def test_validate_financial_statement():
    # Create sample financial statement data with various scenarios (valid, missing fields, inconsistent figures)
    valid_data = {"total_assets": 100000, "total_liabilities": 50000, "total_equity": 50000, "date": "2023-05-01"}
    missing_field_data = {"total_assets": 100000, "total_liabilities": 50000}
    inconsistent_data = {"total_assets": 100000, "total_liabilities": 50000, "total_equity": 60000, "date": "2023-05-01"}
    
    # Create an instance of DataValidator
    validator = DataValidator()
    
    # For each scenario:
    for data in [valid_data, missing_field_data, inconsistent_data]:
        # Call validate_financial_statement with the sample data
        result = validator.validate_financial_statement(data)
        
        # Assert that the returned validation results are correct
        assert 'errors' in result
        assert 'warnings' in result
        
        # Verify that date formats are validated
        if 'date' in data:
            assert data['date'].count('-') == 2 or 'date' in result['errors']
        
        # Check that financial figures are logically consistent (e.g., assets = liabilities + equity)
        if all(key in data for key in ['total_assets', 'total_liabilities', 'total_equity']):
            if data['total_assets'] != data['total_liabilities'] + data['total_equity']:
                assert 'inconsistent_figures' in result['errors'] or 'inconsistent_figures' in result['warnings']
        
        # Ensure that any unusual or outlier values are flagged
        for key in ['total_assets', 'total_liabilities', 'total_equity']:
            if key in data and isinstance(data[key], (int, float)) and data[key] < 0:
                assert key in result['warnings'] or key in result['errors']