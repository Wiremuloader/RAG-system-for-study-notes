# tests/

Pytest test suite for the project. All files here currently exist as empty placeholders and have no implemented tests yet.

## Intended coverage (by filename)

- **`test_loaders.py`** — Should cover `src/ingestion/loaders.py` (PDF loading behavior, handling of missing/invalid files).
- **`test_chunker.py`** — Should cover `src/ingestion/chunker.py` (chunk size/overlap behavior on sample documents).
- **`test_retrieval.py`** — Should cover `src/retrieval/retriever.py` (query embedding + Chroma query behavior, likely against a small seeded/mock collection rather than the full production DB).
- **`test_rag_chain.py`** — Should cover `src/generation/rag_chain.py` end-to-end, likely mocking `llm_client.generate` to avoid depending on a running Ollama instance in CI.

## Running tests
```powershell
pip install pytest
pytest
```
(No tests currently run any assertions — this will report 0 collected tests until the files above are filled in.)
