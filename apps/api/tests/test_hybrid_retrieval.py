from uuid import uuid4

from app.vectorstore import (
    ChromaVectorStore,
    DeterministicEmbeddingProvider,
    HybridRetriever,
    LexicalRetriever,
    ReciprocalRankFusion,
    VectorDocument,
    VectorSearchResult,
)
from app.vectorstore.lexical import LexicalSearchResult


def test_lexical_retriever_scores_exact_terms_and_filters_metadata() -> None:
    retriever = LexicalRetriever()
    retriever.index_documents(
        [
            VectorDocument(
                id="source-1",
                text="Hybrid retrieval combines keyword evidence with semantic vector search.",
                metadata={"run_id": "run-1", "publisher": "research_team"},
            ),
            VectorDocument(
                id="source-2",
                text="Finance operations need approval routing and payroll checks.",
                metadata={"run_id": "run-2", "publisher": "ops_team"},
            ),
        ]
    )

    results = retriever.search("hybrid keyword retrieval", limit=5, where={"run_id": "run-1"})

    assert [result.id for result in results] == ["source-1"]
    assert results[0].matched_terms == ["hybrid", "keyword", "retrieval"]
    assert results[0].score > 0


def test_reciprocal_rank_fusion_rewards_results_seen_by_both_retrievers() -> None:
    fusion = ReciprocalRankFusion(rank_constant=10)
    vector_results = [
        VectorSearchResult(id="shared", text="Shared evidence", metadata={}, distance=0.1, score=0.9),
        VectorSearchResult(id="vector-only", text="Vector evidence", metadata={}, distance=0.2, score=0.8),
    ]
    lexical_results = [
        LexicalSearchResult(id="shared", text="Shared evidence", metadata={}, score=2.0, matched_terms=["evidence"]),
        LexicalSearchResult(id="lexical-only", text="Lexical evidence", metadata={}, score=1.8, matched_terms=["evidence"]),
    ]

    results = fusion.fuse(vector_results=vector_results, lexical_results=lexical_results, limit=3)

    assert results[0].id == "shared"
    assert results[0].vector_rank == 1
    assert results[0].lexical_rank == 1
    assert results[1].id in {"vector-only", "lexical-only"}


def test_hybrid_retriever_indexes_documents_and_returns_fused_results(tmp_path) -> None:
    retriever = HybridRetriever(
        vector_store=ChromaVectorStore(
            persist_directory=str(tmp_path / "chroma"),
            collection_name=f"research_sources_{uuid4().hex}",
            embedding_provider=DeterministicEmbeddingProvider(dimensions=32),
        )
    )

    retriever.index_documents(
        [
            VectorDocument(
                id="source-1",
                text="Hybrid retrieval uses reciprocal rank fusion for vector and keyword search.",
                metadata={"run_id": "run-1", "source_type": "architecture_note"},
            ),
            VectorDocument(
                id="source-2",
                text="Human approval checkpoints keep generated reports under reviewer control.",
                metadata={"run_id": "run-1", "source_type": "workflow_note"},
            ),
            VectorDocument(
                id="source-3",
                text="Customer billing workflows require invoice reconciliation.",
                metadata={"run_id": "run-2", "source_type": "finance_note"},
            ),
        ]
    )

    results = retriever.search(
        query="hybrid retrieval rank fusion keyword vector",
        limit=2,
        where={"run_id": "run-1"},
    )

    assert results[0].id == "source-1"
    assert results[0].vector_rank is not None
    assert results[0].lexical_rank is not None
    assert "fusion" in results[0].matched_terms
    assert all(result.metadata["run_id"] == "run-1" for result in results)
