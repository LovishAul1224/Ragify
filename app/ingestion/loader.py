from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFLoader:
    """Loads PDF files from a directory."""

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

    def load_documents(self) -> list[Document]:
        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Expected a PDF file, got: {self.pdf_path.suffix}"
            )

        loader = PyPDFLoader(str(self.pdf_path))

        return loader.load()