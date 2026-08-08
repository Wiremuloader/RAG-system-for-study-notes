from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from vectorStore.chroma_client import get_collection


def upsert_test_chunks():
    collection = get_collection("study-notes")

    sample_chunks = [
        "A neural network learns patterns from data through repeated adjustments.",
        "Chroma is a vector database that stores embeddings for semantic search.",
        "Study notes can be retrieved efficiently when chunked into meaningful passages.",
    ]

    embeddings = [
        [0.1, 0.2, 0.3, 0.4],
        [0.2, 0.1, 0.4, 0.3],
        [0.3, 0.4, 0.1, 0.2],
    ]

    ids = [f"chunk-{i}" for i in range(len(sample_chunks))]
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=sample_chunks,
    )

    count = collection.count()
    print(f"Inserted {count} documents into collection 'study-notes'.")


if __name__ == "__main__":
    upsert_test_chunks()
