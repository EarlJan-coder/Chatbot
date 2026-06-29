import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")
TIMEOUT = float(os.getenv("TIMEOUT", 120))
SAVE_FILE = os.path.join(os.path.dirname(__file__), "conversation.json")

if not OLLAMA_URL or not MODEL:
    raise ValueError("Missing key")