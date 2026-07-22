from app.ingestion.loader import PDFLoader
from app.ingestion.splitter import DocumentSplitter
from app.ingestion.embeddings import EmbeddingModel
from app.ingestion.vector_store import VectorStore


class IngestionPipeline:
    def __init__(self, pdf_directory: str):
        self.loader = PDFLoader(pdf_directory)
        self.splitter = DocumentSplitter()
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(
            self.embedding_model.get_embeddings()
        )

    def run(self):

        print("Loading PDFs...")
        documents = self.loader.load_documents()

        print(f"Loaded {len(documents)} pages")

        print("Splitting Documents...")
        chunks = self.splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks")

##  resetting chroma collections.
        self.vector_store.reset_collection()


        print("Storing in ChromaDB...")

        self.vector_store.add_documents(chunks)

        print("Done!")

        print(
            f"Collection contains {self.vector_store.get_collection_count()} documents."
        )