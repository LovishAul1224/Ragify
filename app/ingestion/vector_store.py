from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from app.config import CHROMA_DB_DIR, COLLECTION_NAME


class VectorStore:


    def __init__(
        self,
        embedding_model: Embeddings,
        persist_directory: str = CHROMA_DB_DIR,
        collection_name: str = COLLECTION_NAME,
    ):
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            persist_directory=persist_directory,
        )

    def add_documents(self, documents: list[Document]) -> None:
        self.vector_store.add_documents(documents)

    def get_collection_count(self) -> int:
        return self.vector_store._collection.count()
    