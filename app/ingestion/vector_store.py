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

        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_model,
            persist_directory=self.persist_directory,
        )

    def add_documents(
        self,
        documents: list[Document]
    ) -> None:

        self.vector_store.add_documents(documents)

    def get_collection_count(self) -> int:

        return self.vector_store._collection.count()
    

    def document_exists(
        self,
        document_id: str,
    ) -> bool:

        results = self.vector_store.get(
            where={
                "document_id": document_id
            },
            limit=1,
        )

        return len(results["ids"]) > 0

    def delete_document(
        self,
        document_id: str,
    ) -> None:

        self.vector_store._collection.delete(
            where={
                "document_id": document_id
            }
        )


    def reset_collection(self) -> None:

        # Get all document IDs
        result = self.vector_store.get()

        ids = result.get("ids", [])

        if ids:
            self.vector_store.delete(ids=ids)