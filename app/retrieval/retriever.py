from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.ingestion.embeddings import EmbeddingModel
from app.config import TOP_K

class Retriever:
    def __init__(
          self,
          persist_directory="chroma_db",
          collection_name="smart_rag"  
    ):
        embedding_model = EmbeddingModel().get_embeddings()

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            persist_directory=persist_directory,
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k":TOP_K}
        )
        
    def retrieve(
            self,
            query: str,
    )-> list[Document]:
        return self.retriever.invoke(query)
    

    def retrieve_with_score(self,query:str,k: int=5):
        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

