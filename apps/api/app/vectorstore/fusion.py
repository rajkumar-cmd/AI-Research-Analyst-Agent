from app.vectorstore.lexical import LexicalSearchResult
from app.vectorstore.types import HybridSearchResult, VectorSearchResult


class ReciprocalRankFusion:
    def __init__(self, rank_constant: int = 60, vector_weight: float = 1.0, lexical_weight: float = 1.0) -> None:
        if rank_constant < 1:
            raise ValueError("Rank constant must be at least 1.")
        if vector_weight <= 0 or lexical_weight <= 0:
            raise ValueError("Fusion weights must be positive.")

        self.rank_constant = rank_constant
        self.vector_weight = vector_weight
        self.lexical_weight = lexical_weight

    def fuse(
        self,
        vector_results: list[VectorSearchResult],
        lexical_results: list[LexicalSearchResult],
        limit: int,
    ) -> list[HybridSearchResult]:
        if limit < 1:
            raise ValueError("Fusion limit must be at least 1.")

        merged: dict[str, _FusionAccumulator] = {}

        for rank, result in enumerate(vector_results, start=1):
            accumulator = merged.setdefault(
                result.id,
                _FusionAccumulator(id=result.id, text=result.text, metadata=result.metadata),
            )
            accumulator.vector_rank = rank
            accumulator.vector_score = result.score
            accumulator.score += self.vector_weight / (self.rank_constant + rank)

        for rank, result in enumerate(lexical_results, start=1):
            accumulator = merged.setdefault(
                result.id,
                _FusionAccumulator(id=result.id, text=result.text, metadata=result.metadata),
            )
            accumulator.lexical_rank = rank
            accumulator.lexical_score = result.score
            accumulator.matched_terms = result.matched_terms
            accumulator.score += self.lexical_weight / (self.rank_constant + rank)

        fused_results = [
            HybridSearchResult(
                id=accumulator.id,
                text=accumulator.text,
                metadata=accumulator.metadata,
                score=accumulator.score,
                vector_rank=accumulator.vector_rank,
                lexical_rank=accumulator.lexical_rank,
                vector_score=accumulator.vector_score,
                lexical_score=accumulator.lexical_score,
                matched_terms=accumulator.matched_terms,
            )
            for accumulator in merged.values()
        ]

        return sorted(
            fused_results,
            key=lambda result: (
                -result.score,
                result.vector_rank is None,
                result.lexical_rank is None,
                result.vector_rank or 9999,
                result.lexical_rank or 9999,
                result.id,
            ),
        )[:limit]


class _FusionAccumulator:
    def __init__(self, id: str, text: str, metadata: dict[str, object]) -> None:
        self.id = id
        self.text = text
        self.metadata = metadata
        self.score = 0.0
        self.vector_rank: int | None = None
        self.lexical_rank: int | None = None
        self.vector_score: float | None = None
        self.lexical_score: float | None = None
        self.matched_terms: list[str] = []
