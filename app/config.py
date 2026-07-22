from pathlib import Path

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