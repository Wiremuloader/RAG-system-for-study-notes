import json
from pathlib import Path
import sys

from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion.chunker import chunk_pdf_document
from ingestion.loaders import load_pdf_document
from utils.file_hash import hash_file
from vectorStore.chroma_client import get_collection

MANIFEST_PATH = ROOT.parent / "data" / "processed" / "ingested_manifest.json"
RAW_DIR = ROOT.parent / "data" / "raw"
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def build_embeddings(chunks):
    texts = [chunk.page_content for chunk in chunks]
    return _model.encode(texts, normalize_embeddings=True)


def _load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _resolve_pdf_paths(source) -> list[Path]:
    if source is not None:
        source = Path(source)
        if source.is_dir():
            return sorted(source.glob("*.pdf"))
        return [source]

    return sorted(RAW_DIR.glob("*.pdf"))


def ingest_pdf_to_chroma(source=None, collection_name: str = "study-notes", force: bool = False):
    """Ingest one PDF file or every PDF in a folder, skipping files that are unchanged since the last run."""
    pdf_paths = _resolve_pdf_paths(source)
    if not pdf_paths:
        print(f"No PDF files found for source={source!r}")
        return None

    collection = get_collection(collection_name)
    manifest = _load_manifest()

    ingested = 0
    skipped = 0

    for path in pdf_paths:
        file_hash = hash_file(path)
        if not force and manifest.get(path.name) == file_hash:
            skipped += 1
            continue

        # Remove any previously ingested chunks for this file before re-adding, so edited
        # files don't leave stale chunks behind (e.g. if the new version has fewer chunks).
        collection.delete(where={"source": path.name})

        docs = load_pdf_document(None, pdf_path=path)
        if not docs:
            continue
        chunks = chunk_pdf_document(docs)
        if not chunks:
            continue
        embeddings = build_embeddings(chunks)
        ids = [f"{path.stem}-chunk-{i}" for i in range(len(chunks))]

        collection.upsert(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=[chunk.page_content for chunk in chunks],
            metadatas=[{"source": path.name} for _ in chunks],
        )

        manifest[path.name] = file_hash
        ingested += 1

    _save_manifest(manifest)

    print(
        f"Ingested {ingested} file(s), skipped {skipped} unchanged file(s). "
        f"Collection '{collection_name}' now has {collection.count()} chunks."
    )
    return collection


if __name__ == "__main__":
    ingest_pdf_to_chroma()