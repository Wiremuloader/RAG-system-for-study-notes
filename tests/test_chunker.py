from pathlib import Path

from ingestion.chunker import chunk_pdf_document
from ingestion.loaders import load_pdf_document

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def test_chunk_pdf_document_splits_into_chunks():
    pdfs = sorted(RAW_DIR.glob("*.pdf"))
    assert pdfs, "expected at least one PDF in data/raw for this smoke test"

    docs = load_pdf_document(None, pdf_path=pdfs[0])
    chunks = chunk_pdf_document(docs)

    assert len(chunks) >= 1
    assert all(chunk.page_content.strip() for chunk in chunks)
    assert all(len(chunk.page_content) <= 900 for chunk in chunks)  # chunk_size=800 + overlap slack
