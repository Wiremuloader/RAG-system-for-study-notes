from pathlib import Path

import chromadb

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "chroma_db"
client = chromadb.PersistentClient(path=str(DB_PATH))


def get_collection(collection_name: str = "study-notes", recreate: bool = False):
    """Return a Chroma collection, recreating it when requested."""
    if recreate:
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

    try:
        return client.get_collection(name=collection_name)
    except Exception:
        return client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )