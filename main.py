from app.ingestion.ingest import IngestionPipeline


def main():
    pipeline = IngestionPipeline("data/pdfs")
    pipeline.run()


if __name__ == "__main__":
    main()