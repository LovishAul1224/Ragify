from langchain_chroma import Chroma
from app.ingestion.embeddings import EmbeddingModel
from app.config import (
    TOP_K,
    CHROMA_DB_DIR,
    COLLECTION_NAME,
)


class Retriever:

    def __init__(self):

        embedding_model = (
            EmbeddingModel().get_embeddings()
        )

        self.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_model,
            persist_directory=CHROMA_DB_DIR,
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={
                "k": TOP_K
            }
        )

    def retrieve_with_score(
        self,
        query: str,
        k: int = 5,
    ):

        return (
            self.vector_store
            .similarity_search_with_score(
                query=query,
                k=k,
            )
        )