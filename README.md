
# Ragify- Retrieval Augmented Generation System using ChromaDB 

### Hi! Welcome to my project. This is a RAG System which can tell you all the information about the Research Paper Named "Attention is all you Need".


This project is an example that was build while learning and  which will teach you that how to build your own customize RAG. 

# Architecture

<p align="center">
  <a href="assets/architecture.png">
    <img src="assets/architecture.png" alt="System Architecture" width="70%" >
  </a>
</p>


# Tech Stack

**Programming Language:** Python 

**LLM Framework:** LangChain

**Vector Database:** ChromaDB

**LLM:** Ollama

**Backend:** FastAPI

**Frontend:** Streamlit

**Embedding Model:** sentence-transformers

**Document Loader:** LangChain Loaders

**Chunking:** RecursiveCharacterTextSplitter

**Environment Management:** uv

**Version Control:** Git & GitHub






# How It Works


 1. PDF documents are loaded from the `data/pdfs` directory.

2. Documents are split into smaller chunks.
3. Each chunk is converted into embeddings.
4. Embeddings are stored in ChromaDB.
5. User queries are embedded and matched against stored chunks.
6. Relevant context is sent to the LLM to generate grounded answers.
7. If the text is Irrelevant then it will search from the Web.


## Installation

```bash
git clone <repo-url>
cd <project>
```

### 2. Create virtual environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv sync
```

<!-- ## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_key_here
``` -->

## Run the Project

### Step 1: Ingest documents

```bash
uv run main.py
```

# 🚧 PROJECT UNDER MAINTAINANCE 