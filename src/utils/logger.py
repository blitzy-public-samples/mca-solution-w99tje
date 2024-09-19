import logging
import sys
from src.core.config import settings

# Create a logger instance
logger = logging.getLogger(__name__)

def setup_logger():
    """
    Set up the logger for the application
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Set the logging level based on the DEBUG setting in config
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(log_level)

    # Create a StreamHandler for console output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Create a Formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set the formatter for the handler
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Return the configured logger
    return logger