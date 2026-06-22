from collections.abc import Sequence
from pathlib import Path
from typing import Any

import chromadb

from app.vectorstore.embeddings import DeterministicEmbeddingProvider, EmbeddingProvider
from app.vectorstore.types import VectorDocument, VectorSearchResult

MetadataValue = str | int | float | bool


class ChromaVectorStore:
    def __init__(
        self,
        persist_directory: str,
        collection_name: str,
        embedding_provider: EmbeddingProvider | None = None,
    ) -> None:
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.embedding_provider = embedding_provider or DeterministicEmbeddingProvider()
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def index_documents(self, documents: Sequence[VectorDocument]) -> int:
        if not documents:
            return 0

        ids = [document.id for document in documents]
        texts = [document.text for document in documents]
        metadatas = [_clean_metadata(document.metadata) for document in documents]
        embeddings = self.embedding_provider.embed_documents(texts)

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )
        return len(documents)

    def search(
        self,
        query: str,
        limit: int = 5,
        where: dict[str, MetadataValue] | None = None,
    ) -> list[VectorSearchResult]:
        if limit < 1:
            raise ValueError("Search limit must be at least 1.")

        response = self.collection.query(
            query_embeddings=[self.embedding_provider.embed_query(query)],
            n_results=limit,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        ids = response.get("ids", [[]])[0]
        documents = response.get("documents", [[]])[0]
        metadatas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]

        return [
            VectorSearchResult(
                id=item_id,
                text=document or "",
                metadata=metadata or {},
                distance=float(distance),
                score=max(0.0, 1.0 - float(distance)),
            )
            for item_id, document, metadata, distance in zip(ids, documents, metadatas, distances, strict=True)
        ]

    def clear(self) -> None:
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )


def _clean_metadata(metadata: dict[str, Any]) -> dict[str, MetadataValue]:
    cleaned: dict[str, MetadataValue] = {}
    for key, value in metadata.items():
        if isinstance(value, str | int | float | bool):
            cleaned[key] = value
        elif value is not None:
            cleaned[key] = str(value)

    return cleaned
