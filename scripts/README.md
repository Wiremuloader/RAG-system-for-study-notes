# scripts/

Standalone CLI entry points for maintenance tasks. Each script inserts the project root/`src` onto `sys.path` so it can be run directly with `python scripts/<name>.py` from anywhere.

## Files

- **`ingest_notes.py`** — Main ingestion entry point. Delegates to `src/ingestion/pipeline.ingest_pdf_to_chroma()`, which scans every `*.pdf` in `data/raw/` (or a path passed via `--source`), loads + chunks + embeds each one, and upserts new/changed chunks into the `study-notes` Chroma collection. Unchanged files (tracked via `data/processed/ingested_manifest.json`) are skipped. Run this whenever you add/change PDFs in `data/raw/`:
  ```powershell
  python scripts/ingest_notes.py
  python scripts/ingest_notes.py --source data/raw/some_file.pdf
  python scripts/ingest_notes.py --force   # re-ingest everything, ignoring the manifest
  ```

- **`upsert_test_chunks.py`** — Inserts a handful of hardcoded sample text chunks (with dummy, non-semantic embeddings) directly into the `study-notes` collection. Useful only for smoke-testing that the Chroma connection/upsert path works — the embeddings are not meaningful for real similarity search, so don't use this as a substitute for `ingest_notes.py`.

- **`reset_db.py`** — Fully resets ingestion state: deletes/recreates the `study-notes` Chroma collection and removes `data/processed/ingested_manifest.json`. Use this when you want a clean slate (e.g. after changing chunking or embedding settings) before running `ingest_notes.py` again.
