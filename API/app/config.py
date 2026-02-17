"""
Configuration settings for the Annuity Review API
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "Annuity Review API"
    API_VERSION: str = "1.0.0"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:4200",  # Angular dev server
        "http://localhost:3000",
        "http://127.0.0.1:4200",
    ]
    
    # Data paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CLIENTS_DATA_FILE: Path = DATA_DIR / "clients_profile.json"
    POLICIES_DATA_FILE: Path = DATA_DIR / "policies.json"
    PRODUCTS_DATA_FILE: Path = DATA_DIR / "products.json"
    
    # AI Settings (for future implementation)
    AI_PROVIDER: str = "openai"  # openai, anthropic, azure-openai, mock
    AI_MODEL: str = "gpt-4"
    AI_API_KEY: str = ""
    AI_MOCK_MODE: bool = True  # Use mock responses for hackathon
    
    # Alert Engine Settings
    REPLACEMENT_RENEWAL_DAYS_THRESHOLD: int = 30
    REPLACEMENT_CAP_DROP_THRESHOLD: float = 0.5  # percentage points
    INCOME_ACTIVATION_AGE_THRESHOLD: int = 59
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
