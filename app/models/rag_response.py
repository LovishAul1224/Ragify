from dataclasses import dataclass

@dataclass
class RAGResponse:
    answer: str
    is_relevant: bool
    similarity_score: float
    source: str
    page: int
    from_web: bool = False