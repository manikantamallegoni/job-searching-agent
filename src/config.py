import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration management for the AI Job Searching Agent."""

    # API Keys
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


    # Model Configuration
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL = "openai/gpt-4o-mini"

    @classmethod
    def validate(cls):
        """Validates that required credentials exist."""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("⚠️ Missing OPENROUTER_API_KEY in environment variables (.env file).")