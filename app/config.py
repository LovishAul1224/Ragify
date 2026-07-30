from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_NAME = "deepseek/deepseek-chat-v3"

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

TEMPERATURE = 0

SIMILARITY_THRESHOLD = 1.20

# -------------------------
# Project Paths
# -------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"

CHROMA_DB_DIR = BASE_DIR / "chroma_db"

# -------------------------
# ChromaDB
# -------------------------

COLLECTION_NAME = "smart_rag"

# -------------------------
# Text Splitting
# -------------------------

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# -------------------------
# Embedding Model
# -------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -------------------------
# Retrieval
# -------------------------

TOP_K = 5