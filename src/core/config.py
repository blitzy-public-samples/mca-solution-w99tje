from pydantic import BaseSettings, SecretStr
from typing import List

class Settings(BaseSettings):
    # Project configuration
    PROJECT_NAME: str
    API_V1_STR: str
    SECRET_KEY: SecretStr
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Database configuration
    DATABASE_URL: str

    # Security configuration
    ALLOWED_HOSTS: List[str]

    # AWS configuration
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: SecretStr
    AWS_REGION: str
    S3_BUCKET_NAME: str

    # Email configuration
    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: SecretStr
    EMAIL_FROM: str

    class Config:
        case_sensitive = True
        env_file = '.env'

    def __init__(self, **kwargs):
        # Initialize all settings with default values or environment variables
        super().__init__(**kwargs)

# Create a global instance of the Settings class
settings = Settings()