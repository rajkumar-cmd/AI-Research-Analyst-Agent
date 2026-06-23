from app.core.config import Settings, get_settings
from app.vectorstore.chroma import ChromaVectorStore
from app.vectorstore.embeddings import DeterministicEmbeddingProvider, EmbeddingProvider
from app.vectorstore.hybrid import HybridRetriever


def get_vector_store(
    settings: Settings | None = None,
    embedding_provider: EmbeddingProvider | None = None,
) -> ChromaVectorStore:
    settings = settings or get_settings()
    return ChromaVectorStore(
        persist_directory=settings.chroma_persist_directory,
        collection_name=settings.chroma_collection_name,
        embedding_provider=embedding_provider or DeterministicEmbeddingProvider(settings.embedding_dimensions),
    )


def get_hybrid_retriever(
    settings: Settings | None = None,
    embedding_provider: EmbeddingProvider | None = None,
) -> HybridRetriever:
    return HybridRetriever(vector_store=get_vector_store(settings=settings, embedding_provider=embedding_provider))
