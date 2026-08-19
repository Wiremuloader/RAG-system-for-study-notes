"""Cross-encoder reranking for retrieved chunks, used when vector similarity alone is too fuzzy."""

from sentence_transformers import CrossEncoder

_cross_encoder = None


def _get_cross_encoder():
    global _cross_encoder
    if _cross_encoder is None:
        _cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _cross_encoder


def rerank_chunks(question: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    """Re-score retrieved chunks against the question and return the top_k most relevant."""
    if not candidates:
        return candidates

    cross_encoder = _get_cross_encoder()
    pairs = [(question, c["document"]) for c in candidates]
    scores = cross_encoder.predict(pairs)

    for candidate, score in zip(candidates, scores):
        candidate["rerank_score"] = float(score)

    return sorted(candidates, key=lambda c: c["rerank_score"], reverse=True)[:top_k]
