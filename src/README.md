# src/

Core library code for the RAG pipeline, organized by stage. Each subpackage has its own `__init__.py` and is imported via `sys.path` manipulation at each entry point's top (rather than an installed package), so scripts add either the project root or `src/` to `sys.path` before importing.

## Subpackages

- **`ingestion/`** — Turning raw PDFs into embedded, stored chunks.
  - `loaders.py` — `load_pdf_document()` loads a single PDF via `PyPDFLoader` (image extraction disabled, since some scanned slide PDFs break on embedded images).
  - `chunker.py` — `chunk_pdf_document()` splits loaded documents into ~500-character chunks (50-char overlap) using `CharacterTextSplitter`.
  - `pipeline.py` — `ingest_pdf_to_chroma()` ties loading + chunking + embedding + Chroma upsert together. Defaults to scanning every PDF in `data/raw/` when no explicit path is given, recreating the target collection so re-runs are idempotent.

- **`embeddings/`** — `embedding.py` currently defines `get_embedding_model()` using `langchain`'s `OpenAIEmbeddings`. This is **not** what the pipeline actually uses (ingestion/retrieval embed directly with `sentence-transformers` for a fully local, API-key-free setup) — treat this file as stale/unused unless you intentionally wire in an OpenAI-backed embedding path.

- **`vectorStore/`** — Chroma persistence layer.
  - `chroma_client.py` — `get_collection(name, recreate=False)` returns (or creates) a Chroma collection backed by a `PersistentClient` pointed at `data/chroma_db/`, using cosine similarity (`hnsw:space: cosine`).
  - `operations.py` — Currently empty; reserved for additional vector store operations (e.g. delete-by-source, update single documents) beyond the basic upsert used today.

- **`retrieval/`** — Turning a question into relevant chunks.
  - `retriever.py` — `query_chroma(question, top_k=5, collection_name="study-notes")` embeds the question with the same `all-MiniLM-L6-v2` model used at ingestion time, queries Chroma, and returns a list of `{"document", "distance", "source"}` dicts.
  - `retriever_test.py` — A quick manual smoke test: runs a few hardcoded questions through `query_chroma()` and prints the results so you can eyeball relevance without invoking an LLM.
  - `reranker.py` — Currently empty; reserved for an optional re-ranking step (e.g. cross-encoder re-scoring) applied after the initial vector similarity retrieval.

- **`generation/`** — Turning retrieved chunks + a question into a grounded answer.
  - `prompt_templates.py` — `build_prompt(question, retrieved_chunks)` formats numbered, source-labeled context blocks and instructs the model to answer only from that context (and say "I don't know" otherwise).
  - `llm_client.py` — `generate(prompt, model=...)` calls a local [Ollama](https://ollama.com) server's `/api/generate` HTTP endpoint. Default model is `qwen2.5:7b-instruct`; change `DEFAULT_MODEL` to swap models.
  - `rag_chain.py` — `answer_question(question, top_k=5)` is the top-level orchestration function: retrieve → build prompt → generate → return `{"answer", "chunks"}`. This is what `app/streamlit_app.py` calls.

- **`utils/`** — Cross-cutting helpers.
  - `file_hash.py` — Currently empty; reserved for hashing ingested files (e.g. to skip re-ingesting unchanged PDFs).
  - `logging_config.py` — Currently empty; reserved for centralized logging setup.

## Import convention
Files in `src/` are written assuming `src/` itself (not the project root) is on `sys.path`, so they use imports like `from ingestion.chunker import chunk_pdf_document` rather than `from src.ingestion.chunker import ...`. Scripts calling into `src/` from outside (e.g. `scripts/ingest_notes.py`) instead import via the `src.` prefix after adding the project root to `sys.path`. Keep this distinction in mind when adding new modules or scripts.
