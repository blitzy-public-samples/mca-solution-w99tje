import pytest
from unittest.mock import Mock, patch
from fastapi import UploadFile
from src.utils.helpers import save_upload_file, remove_file, format_currency, validate_email, sanitize_input
from src.core.config import settings

@pytest.mark.asyncio
async def test_save_upload_file():
    # Create a mock UploadFile object
    mock_file = Mock(spec=UploadFile)
    mock_file.filename = "test_file.txt"
    mock_file.file.read.return_value = b"Test content"

    # Mock the open function to simulate file writing
    with patch("builtins.open", mock_open()) as mock_file_open:
        # Mock uuid4 to return a predictable value
        with patch("uuid.uuid4", return_value="1234-5678"):
            # Call save_upload_file with the mock UploadFile
            result = await save_upload_file(mock_file)

    # Assert that the file was 'saved' to the correct location
    expected_path = f"{settings.UPLOAD_DIR}/1234-5678_test_file.txt"
    mock_file_open.assert_called_once_with(expected_path, "wb")
    mock_file_open().write.assert_called_once_with(b"Test content")

    # Verify that the returned path is correct
    assert result == expected_path

def test_remove_file():
    # Mock the os.path.exists function
    with patch("os.path.exists") as mock_exists:
        # Mock the os.remove function
        with patch("os.remove") as mock_remove:
            # Test removing an existing file
            mock_exists.return_value = True
            remove_file("/path/to/existing_file.txt")
            mock_remove.assert_called_once_with("/path/to/existing_file.txt")

            # Test attempting to remove a non-existent file
            mock_exists.return_value = False
            remove_file("/path/to/non_existent_file.txt")
            # Verify that os.remove was not called for non-existent files
            assert mock_remove.call_count == 1

def test_format_currency():
    # Test formatting various amounts with different currency symbols
    assert format_currency(1000, "$") == "$1,000.00"
    assert format_currency(1234567.89, "£") == "£1,234,567.89"
    assert format_currency(0.50, "€") == "€0.50"
    assert format_currency(1000000, "¥") == "¥1,000,000.00"

    # Verify correct handling of whole numbers
    assert format_currency(42, "$") == "$42.00"

    # Verify correct handling of decimal numbers
    assert format_currency(42.42, "$") == "$42.42"

    # Verify correct placement of currency symbol
    assert format_currency(100, "kr") == "kr100.00"

    # Verify correct thousands separator
    assert format_currency(1234567, "$") == "$1,234,567.00"

def test_validate_email():
    # Test with valid email addresses
    assert validate_email("user@example.com") == True
    assert validate_email("user.name+tag@example.co.uk") == True
    assert validate_email("user123@subdomain.example.com") == True

    # Test with invalid email addresses
    assert validate_email("invalid_email") == False
    assert validate_email("user@") == False
    assert validate_email("@example.com") == False
    assert validate_email("user@example") == False
    assert validate_email("user@.com") == False

    # Verify correct validation of various email formats
    assert validate_email("user-name@example-domain.com") == True
    assert validate_email("user_name@example.domain.com") == True

    # Verify rejection of improperly formatted emails
    assert validate_email("user name@example.com") == False
    assert validate_email("user@example..com") == False

def test_sanitize_input():
    # Test with input containing HTML special characters
    assert sanitize_input("<script>alert('XSS')</script>") == "&lt;script&gt;alert('XSS')&lt;/script&gt;"
    assert sanitize_input("This & that") == "This &amp; that"

    # Test with input containing potential XSS payloads
    assert sanitize_input('<img src="x" onerror="alert(\'XSS\')">') == '&lt;img src="x" onerror="alert(\'XSS\')"&gt;'
    assert sanitize_input('javascript:alert("XSS")') == 'javascript:alert("XSS")'

    # Verify that HTML special characters are properly escaped
    assert sanitize_input('<>"\'&') == "&lt;&gt;&quot;&#x27;&amp;"

    # Verify that the sanitized output doesn't contain executable scripts
    sanitized = sanitize_input('<script>document.cookie</script>')
    assert '<script>' not in sanitized
    assert '</script>' not in sanitized