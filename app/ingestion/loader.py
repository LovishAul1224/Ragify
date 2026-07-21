from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFLoader:
    """Loads PDF files from a directory."""

    def __init__(self, pdf_directory: str):
        self.pdf_directory = Path(pdf_directory)

    def load_documents(self) -> list[Document]:
        documents = []

        pdf_files = self.pdf_directory.glob("*.pdf")

        for pdf_file in pdf_files:
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            documents.extend(docs)
        
        return documents