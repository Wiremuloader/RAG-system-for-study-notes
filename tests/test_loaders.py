from pathlib import Path

from ingestion.loaders import load_pdf_document

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def _first_pdf() -> Path:
    pdfs = sorted(RAW_DIR.glob("*.pdf"))
    assert pdfs, "expected at least one PDF in data/raw for this smoke test"
    return pdfs[0]


def test_load_pdf_document_returns_non_empty_docs():
    docs = load_pdf_document(None, pdf_path=_first_pdf())

    assert len(docs) >= 1
    assert docs[0].page_content.strip() != ""
    assert docs[0].metadata["source"].endswith(".pdf")
