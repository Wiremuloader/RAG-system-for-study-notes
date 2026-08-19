# scripts/

Standalone CLI entry points for maintenance tasks. Each script inserts the project root/`src` onto `sys.path` so it can be run directly with `python scripts/<name>.py` from anywhere.

## Files

- **`ingest_notes.py`** — Main ingestion entry point. Delegates to `src/ingestion/pipeline.ingest_pdf_to_chroma()`, which scans every `*.pdf` in `data/raw/`, loads + chunks + embeds each one, and upserts all chunks into the `study-notes` Chroma collection (recreating it fresh each run). Run this whenever you add/change PDFs in `data/raw/`:
  ```powershell
  python scripts/ingest_notes.py
  ```

- **`upsert_test_chunks.py`** — Inserts a handful of hardcoded sample text chunks (with dummy, non-semantic embeddings) directly into the `study-notes` collection. Useful only for smoke-testing that the Chroma connection/upsert path works — the embeddings are not meaningful for real similarity search, so don't use this as a substitute for `ingest_notes.py`.

- **`reset_db.py`** — Currently an empty placeholder. Intended to fully wipe/reset the Chroma database (e.g. delete the `study-notes` collection or the whole `data/chroma_db/` directory) without re-ingesting.
