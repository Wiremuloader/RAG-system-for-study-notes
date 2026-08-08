from pathlib import Path
import sys

from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vectorStore.chroma_client import get_collection

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def query_chroma(question: str, top_k: int =5, collection_name: str = "study-notes"):
    collection = get_collection(collection_name)
    
    query_embedding = model.encode([question], normalize_embeddings=True)[0]
    
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "distances"]
    )
    
    docs = results["documents"][0]
    distance = results["distances"][0]
    
    return [
        {"document": doc, "distance": dist} for doc, dist in zip(docs, distance)
    ]