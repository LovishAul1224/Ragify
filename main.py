from app.config import PDF_DIR
from app.ingestion.ingest import IngestionPipeline
from app.services.rag_service import RAGService

def main():
    pipeline = IngestionPipeline(PDF_DIR)
    pipeline.run()



if __name__ == "__main__":
    main()