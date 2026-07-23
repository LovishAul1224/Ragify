from app.ingestion.ingest import IngestionPipeline
from app.config import PDF_DIR
from app.retrieval.retriever import Retriever

def main():
    pipeline = IngestionPipeline(PDF_DIR)
    pipeline.run()

    retriever = Retriever()

    results = retriever.retrieve_with_score(
        "What is self attention?"
    )
    
    for i, (doc, score) in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Score: {score}")
        print(f"Page: {doc.metadata['page']}")
        print(f"Source: {doc.metadata['source']}")
        print(f"Content:\n{doc.page_content[:300]}")
        print("-" * 80)


if __name__ == "__main__":
    main()