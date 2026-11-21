"""
RAG retrieval tests verifying CPCB & WHO guideline grounding.
"""
from pathlib import Path
import pytest

from app.services.rag_retriever import KnowledgeIndex, RetrievedChunk


@pytest.fixture
def retriever():
    path = Path("data/processed/chunks.jsonl")
    return KnowledgeIndex(chunks_path=path)


class TestRAGRetrieval:
    def test_who_pm25_guideline_retrieval(self, retriever: KnowledgeIndex) -> None:
        results = retriever.retrieve("WHO PM2.5 annual guideline 24-hour limit", top_k=3)
        assert len(results) >= 1
        top_match = results[0]
        assert isinstance(top_match, RetrievedChunk)
        assert "WHO" in top_match.source
        assert "5" in top_match.text

    def test_cpcb_naaqs_standards(self, retriever: KnowledgeIndex) -> None:
        results = retriever.retrieve("CPCB NAAQS standards 24-hour PM2.5", top_k=3)
        assert len(results) >= 1
        texts = " ".join(r.text for r in results)
        assert "60" in texts or "CPCB" in texts

    def test_diy_filtration_retrieval(self, retriever: KnowledgeIndex) -> None:
        results = retriever.retrieve("DIY box fan MERV13 filter CADR", top_k=2)
        assert len(results) >= 1
        assert "box fan" in results[0].text.lower() or "cadr" in results[0].text.lower()

    def test_transport_emissions(self, retriever: KnowledgeIndex) -> None:
        results = retriever.retrieve("metro versus two wheeler emissions CO2 NOx", top_k=2)
        assert len(results) >= 1
        texts = " ".join(r.text for r in results)
        assert "Metro" in texts or "Two-wheelers" in texts
