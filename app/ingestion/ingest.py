from app.ingestion.loader import PDFLoader
from app.ingestion.splitter import DocumentSplitter
from app.ingestion.embeddings import EmbeddingModel
from app.ingestion.vector_store import VectorStore
from langchain_community.document_loaders import Blob
from langchain_community.document_loaders.parsers import PyPDFParser


class IngestionPipeline:

    def __init__(self, pdf_path: str | None = None):

        # PDFLoader is only created when a PDF path exists
        self.loader = (
            PDFLoader(pdf_path)
            if pdf_path is not None
            else None
        )

        self.splitter = DocumentSplitter()

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore(
            self.embedding_model.get_embeddings()
        )

    def run(self):

        if self.loader is None:
            raise ValueError(
                "PDF path is required to run ingestion."
            )

        print("Loading PDF...")

        documents = self.loader.load_documents()

        print(f"Loaded {len(documents)} pages")

        print("Splitting Documents...")

        chunks = self.splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks")

        print("Storing in ChromaDB...")

        self.vector_store.add_documents(chunks)

        print("Done!")

        print(
            f"Collection contains "
            f"{self.vector_store.get_collection_count()} documents."
        )

    def reset_collection(self) -> None:

        self.vector_store.reset_collection()

    
    def run_from_bytes(
        self,
        pdf_bytes: bytes,
        file_name: str,
        file_id: str | None = None,
    ):

        print(f"Loading Google Drive PDF: {file_name}")

    # --------------------------------
    # DOCUMENT ID
    # --------------------------------

        if not file_id:
            raise ValueError(
                "Google Drive file_id is required."
            )

        document_id = f"google_drive:{file_id}"

    # --------------------------------
    # CHECK DUPLICATE
    # --------------------------------

        if self.vector_store.document_exists(document_id):

            print(
                f"Skipping {file_name} - "
                f"already exists in ChromaDB."
            )

            return False

    # --------------------------------
    # LOAD PDF FROM MEMORY
    # --------------------------------

        blob = Blob.from_data(
            pdf_bytes,
            path=file_name,
        )

        parser = PyPDFParser()

        documents = list(
            parser.lazy_parse(blob)
        )

        print(f"Loaded {len(documents)} pages")

    # --------------------------------
    # METADATA
    # --------------------------------

        for document in documents:

            document.metadata.update({
                "source": file_name,
                "source_type": "google_drive",
                "google_drive_file_id": file_id,
                "document_id": document_id,
            })

    # --------------------------------
    # SPLIT
    # --------------------------------

        print("Splitting Documents...")

        chunks = self.splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks")

    # --------------------------------
    # MAKE SURE CHUNKS HAVE METADATA
    # --------------------------------

        for chunk in chunks:

            chunk.metadata.update({
                "source": file_name,
                "source_type": "google_drive",
                "google_drive_file_id": file_id,
                "document_id": document_id,
            })

    # --------------------------------
    # STORE
    # --------------------------------

        print("Storing in ChromaDB...")

        self.vector_store.add_documents(chunks)

        print("Done!")

        print(
            f"Collection contains "
            f"{self.vector_store.get_collection_count()} documents."
        )

        return True
