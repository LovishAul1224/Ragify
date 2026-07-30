from app.config import PDF_DIR
from app.ingestion.ingest import IngestionPipeline
from app.services.rag_service import RAGService

def main():
    pipeline = IngestionPipeline(PDF_DIR)
    pipeline.run()


    rag = RAGService()

    query = "What is self attention?"

    response = rag.ask(query)

    print("\nAnswer:")
    print(response.answer)
    print("\nSimilarity Score:")
    print(response.similarity_score)
    print("\nSource:")
    print(response.source)
    print("\nPage:")
    print(response.page)



if __name__ == "__main__":
    main()