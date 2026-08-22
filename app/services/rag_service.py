from pathlib import Path
from app.llm.openrouter import OpenRouterLLM
from app.prompts.rag_prompt import build_prompt
from app.retrieval.retriever import Retriever
from app.config import SIMILARITY_THRESHOLD
from app.models.rag_response import RAGResponse

class RAGService:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = OpenRouterLLM()

    def ask(self, question: str) -> RAGResponse:
        """
        Execute the complete RAG pipeline.

        Steps:
        1. Retrieve relevant documents.
        2. Build the prompt.
        3. Generate an answer using the LLM.

        """

        results = self.retriever.retrieve_with_score(question)

        if not results:
            return RAGResponse(
                answer="No relevant documents found.",
                is_relevant=False,
                similarity_score=float("inf"),
                source="",
                page=-1,
                from_web=False,
            )

        # Find the best (lowest) distance score
        best_doc, best_score = min(
            results,
            key = lambda x: x[1]
        )

        # Threshold check
        if best_score > SIMILARITY_THRESHOLD:
            return RAGResponse(
                answer="I couldn't find the answer in the uploaded documents.",
                is_relevant=False,
                similarity_score=best_score,
                source="",
                page=-1,
                from_web=False,
            )

        # Extract only the documents
        documents = [doc for doc, _ in results]

        prompt = build_prompt(
            question=question,
            documents=documents,
        )

        response = self.llm.generate(prompt)

        return RAGResponse(
            answer=response,
            is_relevant=True,
            similarity_score=best_score,
            source = Path(best_doc.metadata.get("source", "")).name,
            page=best_doc.metadata.get("page", -1),
        )
    