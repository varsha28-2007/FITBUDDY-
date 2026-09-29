"""Shared configuration: loads the .env file and creates Gemini model objects."""
import os
from pathlib import Path

from google import genai
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent  # the fitbuddy/ folder
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PRO_MODEL_NAME = os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-pro")
FLASH_MODEL_NAME = os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash")

_client = None


def get_client() -> genai.Client:
    """Returns a shared google-genai client (HTTPS-based, no grpc dependency)."""
    global _client
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client
