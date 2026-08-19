from pathlib import Path
import sys

from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vectorStore.chroma_client import get_collection

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def query_chroma(
    question: str,
    top_k: int = 5,
    collection_name: str = "study-notes",
    use_reranker: bool = False,
    fetch_k: int = None,
):
    collection = get_collection(collection_name)

    query_embedding = model.encode([question], normalize_embeddings=True)[0]

    # When reranking, over-fetch candidates by vector similarity so the cross-encoder
    # has a wider pool to pick the true top_k from.
    n_results = fetch_k or (top_k * 4 if use_reranker else top_k)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )
    
    docs = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]
    
    candidates = [
        {"document": doc, "distance": dist, "source": meta.get("source")}
        for doc, dist, meta in zip(docs, distances, metadatas)
    ]

    if use_reranker:
        from retrieval.reranker import rerank_chunks
        return rerank_chunks(question, candidates, top_k=top_k)

    return candidates[:top_k]