from collections.abc import Sequence

from app.vectorstore.chroma import ChromaVectorStore, MetadataValue
from app.vectorstore.fusion import ReciprocalRankFusion
from app.vectorstore.lexical import LexicalRetriever
from app.vectorstore.types import HybridSearchResult, VectorDocument


class HybridRetriever:
    def __init__(
        self,
        vector_store: ChromaVectorStore,
        lexical_retriever: LexicalRetriever | None = None,
        rank_fusion: ReciprocalRankFusion | None = None,
        candidate_multiplier: int = 3,
    ) -> None:
        if candidate_multiplier < 1:
            raise ValueError("Candidate multiplier must be at least 1.")

        self.vector_store = vector_store
        self.lexical_retriever = lexical_retriever or LexicalRetriever()
        self.rank_fusion = rank_fusion or ReciprocalRankFusion()
        self.candidate_multiplier = candidate_multiplier

    def index_documents(self, documents: Sequence[VectorDocument]) -> int:
        indexed_count = self.vector_store.index_documents(documents)
        self.lexical_retriever.index_documents(documents)
        return indexed_count

    def search(
        self,
        query: str,
        limit: int = 5,
        where: dict[str, MetadataValue] | None = None,
    ) -> list[HybridSearchResult]:
        if limit < 1:
            raise ValueError("Search limit must be at least 1.")

        candidate_limit = limit * self.candidate_multiplier
        vector_results = self.vector_store.search(query=query, limit=candidate_limit, where=where)
        lexical_results = self.lexical_retriever.search(query=query, limit=candidate_limit, where=where)

        return self.rank_fusion.fuse(
            vector_results=vector_results,
            lexical_results=lexical_results,
            limit=limit,
        )
