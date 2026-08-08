from pathlib import Path
import sys

from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion.chunker import chunk_pdf_document
from ingestion.loaders import load_pdf_document
from vectorStore.chroma_client import get_collection


def build_embeddings(chunks):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    texts = [chunk.page_content for chunk in chunks]
    return model.encode(texts, normalize_embeddings=True)


def ingest_pdf_to_chroma(pdf_path=None, collection_name: str = "study-notes"):
    if pdf_path is None:
        pdf_path = str(Path("data/raw") / "Yamakawa_Fuzzy_Engine_Analog_Mode_Fuzzy_Logic_Control.pdf")

    docs = load_pdf_document(None, pdf_path=pdf_path)
    chunks = chunk_pdf_document(docs)
    embeddings = build_embeddings(chunks)

    collection = get_collection(collection_name, recreate=True)
    ids = [f"chunk-{i}" for i in range(len(chunks))]

    collection.upsert(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=[chunk.page_content for chunk in chunks],
    )

    print(f"Inserted {collection.count()} documents into collection '{collection_name}'.")
    return collection


if __name__ == "__main__":
    ingest_pdf_to_chroma()