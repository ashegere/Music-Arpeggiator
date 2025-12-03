
from pydantic_settings import BaseSettings
from typing import Dict, List

class Settings(BaseSettings):
    APP_NAME: str = "AI Arpeggiator"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Model settings
    USE_GPU: bool = False
    MODEL_NAME: str = "gpt2"
    MAX_PATTERN_LENGTH: int = 32
    
    # Music settings
    MIN_BPM: int = 40
    MAX_BPM: int = 240
    MIN_BARS: int = 1
    MAX_BARS: int = 8
    
    class Config:
        env_file = ".env"

settings = Settings()