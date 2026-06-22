import hashlib
import math
import re
from collections.abc import Sequence
from typing import Protocol

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


class EmbeddingProvider(Protocol):
    dimensions: int

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        pass

    def embed_query(self, text: str) -> list[float]:
        pass


class DeterministicEmbeddingProvider:
    """Small local embedding provider for tests and development fixtures."""

    def __init__(self, dimensions: int = 32) -> None:
        if dimensions < 8:
            raise ValueError("Embedding dimensions must be at least 8.")

        self.dimensions = dimensions

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = TOKEN_PATTERN.findall(text.lower())

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector

        return [value / magnitude for value in vector]
