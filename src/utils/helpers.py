import os
from uuid import uuid4
from typing import Any
from fastapi import UploadFile
from src.core.config import settings
from src.utils.logger import logger
import re
import html

def save_upload_file(upload_file: UploadFile) -> str:
    # Generate a unique filename using UUID
    unique_filename = f"{uuid4()}{os.path.splitext(upload_file.filename)[1]}"
    
    # Create the full file path using the temporary upload directory from settings
    file_path = os.path.join(settings.TEMP_UPLOAD_DIR, unique_filename)
    
    # Open the file for writing in binary mode
    with open(file_path, "wb") as buffer:
        # Write the contents of the upload file to the new file
        buffer.write(upload_file.file.read())
    
    # Log the successful file save
    logger.info(f"File saved successfully: {file_path}")
    
    # Return the full path of the saved file
    return file_path

def remove_file(file_path: str) -> bool:
    # Check if the file exists
    if os.path.exists(file_path):
        try:
            # If file exists, attempt to remove it
            os.remove(file_path)
            # Log the successful file removal
            logger.info(f"File removed successfully: {file_path}")
            return True
        except OSError as e:
            # Log the error if file removal fails
            logger.error(f"Error removing file {file_path}: {str(e)}")
            return False
    else:
        # Log that the file doesn't exist
        logger.warning(f"File not found for removal: {file_path}")
        return False

def format_currency(amount: float, currency_symbol: str) -> str:
    # Round the amount to two decimal places
    rounded_amount = round(amount, 2)
    
    # Format the amount with thousands separator and two decimal places
    formatted_amount = f"{rounded_amount:,.2f}"
    
    # Add the currency symbol to the formatted amount
    return f"{currency_symbol}{formatted_amount}"

def validate_email(email: str) -> bool:
    # Define a regular expression pattern for email validation
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Use re.match to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False

def sanitize_input(input_string: str) -> str:
    # Use html.escape to replace special characters with their HTML entities
    sanitized_string = html.escape(input_string)
    
    # Return the sanitized string
    return sanitized_string