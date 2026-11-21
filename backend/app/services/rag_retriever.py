"""
Authoritative RAG Retriever for VayuMitra:
Indexes CPCB and WHO guidelines, scientific studies, and policy frameworks.
Uses scikit-learn TF-IDF vectorization and normalized cosine similarity for
instant, robust, zero-DLL dependency vector retrieval.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    text: str
    source: str
    page: int
    section: str
    score: float


class KnowledgeIndex:
    """In-memory vector retriever backed by TF-IDF & cosine similarity."""

    def __init__(self, chunks_path: Path | str) -> None:
        self.chunks_path = Path(chunks_path)
        self.chunks: list[dict[str, Any]] = []
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            lowercase=True,
            sublinear_tf=True,
        )
        self.matrix = None
        self._load_and_fit()

    def _load_and_fit(self) -> None:
        if not self.chunks_path.exists():
            return

        with open(self.chunks_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    self.chunks.append(json.loads(line))

        if not self.chunks:
            return

        corpus = [
            f"{c.get('source', '')} {c.get('section', '')} {c.get('text', '')}"
            for c in self.chunks
        ]
        self.matrix = self.vectorizer.fit_transform(corpus)

    def retrieve(self, query: str, top_k: int = 4, min_score: float = 0.05) -> list[RetrievedChunk]:
        """Query the knowledge base and return top matching chunks above min_score."""
        if self.matrix is None or not self.chunks:
            return []

        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]

        # Rank indices by score descending
        ranked_indices = scores.argsort()[::-1]

        results: list[RetrievedChunk] = []
        for idx in ranked_indices:
            score = float(scores[idx])
            if score < min_score:
                break
            chunk = self.chunks[idx]
            results.append(
                RetrievedChunk(
                    text=str(chunk.get("text", "")),
                    source=str(chunk.get("source", "CPCB/WHO Guideline")),
                    page=int(chunk.get("page", 1)),
                    section=str(chunk.get("section", "")),
                    score=round(score, 4),
                )
            )
            if len(results) >= top_k:
                break

        return results
