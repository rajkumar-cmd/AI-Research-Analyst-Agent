from uuid import uuid4

from app.vectorstore import ChromaVectorStore, DeterministicEmbeddingProvider, VectorDocument


def test_chroma_vector_store_indexes_and_searches_documents(tmp_path) -> None:
    store = ChromaVectorStore(
        persist_directory=str(tmp_path / "chroma"),
        collection_name=f"research_sources_{uuid4().hex}",
        embedding_provider=DeterministicEmbeddingProvider(dimensions=32),
    )

    indexed = store.index_documents(
        [
            VectorDocument(
                id="source-1",
                text="Vector databases help SaaS teams retrieve product knowledge for AI agents.",
                metadata={"run_id": "run-1", "source_type": "market_report", "credibility": 0.91},
            ),
            VectorDocument(
                id="source-2",
                text="Payroll compliance rules vary by country and require finance operations review.",
                metadata={"run_id": "run-2", "source_type": "policy_note", "credibility": 0.82},
            ),
        ]
    )

    results = store.search(
        query="vector database retrieval for SaaS AI products",
        limit=2,
        where={"run_id": "run-1"},
    )

    assert indexed == 2
    assert len(results) == 1
    assert results[0].id == "source-1"
    assert results[0].metadata["source_type"] == "market_report"
    assert results[0].score > 0


def test_chroma_vector_store_upserts_existing_document(tmp_path) -> None:
    store = ChromaVectorStore(
        persist_directory=str(tmp_path / "chroma"),
        collection_name=f"research_sources_{uuid4().hex}",
        embedding_provider=DeterministicEmbeddingProvider(dimensions=32),
    )

    store.index_documents(
        [
            VectorDocument(
                id="source-1",
                text="Initial note about broad enterprise software trends.",
                metadata={"run_id": "run-1", "version": 1},
            )
        ]
    )
    store.index_documents(
        [
            VectorDocument(
                id="source-1",
                text="Updated note about AI research agents and citation workflows.",
                metadata={"run_id": "run-1", "version": 2},
            )
        ]
    )

    results = store.search("AI research agents citation workflows", limit=1, where={"run_id": "run-1"})

    assert results[0].id == "source-1"
    assert results[0].metadata["version"] == 2
    assert "citation workflows" in results[0].text
