import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
EMBEDDING_MODEL: str = "embed-multilingual-v3.0"
CHAT_MODEL: str = "command-r-plus-08-2024"
EMBEDDING_DIM: int = 1024

_ROOT = Path(__file__).parent.parent  # src/
DATA_DIR = _ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"

CHUNK_SIZE: int = 800
CHUNK_OVERLAP: int = 150
RETRIEVAL_TOP_K: int = 5
