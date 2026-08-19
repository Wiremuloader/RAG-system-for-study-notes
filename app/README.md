# app/

The Streamlit front-end for the RAG system — a chat interface for asking questions about your ingested lecture slides.

## Run it
```powershell
streamlit run app/streamlit_app.py
```
Requires the `study-notes` Chroma collection to already be populated (see `scripts/ingest_notes.py`) and Ollama running locally for answer generation.

## Files

- **`streamlit_app.py`** — Entry point. Sets up `sys.path` so both `src/` and `app/` are importable, wires `src/generation/rag_chain.answer_question` and `src/ingestion/pipeline.ingest_pdf_to_chroma` into the UI, and renders the page title.

- **`components/chat_ui.py`** — `render_chat(answer_question)`. Owns the chat loop:
  - Keeps message history in `st.session_state.messages` so it persists across reruns within a session.
  - Renders past turns and accepts new questions via `st.chat_input`.
  - On a new question, calls the supplied `answer_question` function, displays the answer, and shows the retrieved chunks via `source_display.render_sources`.

- **`components/source_display.py`** — `render_sources(chunks)`. Renders retrieved chunks in a collapsible "Sources" expander, showing each chunk's source PDF filename, similarity distance, reranker score (when present), and a text preview — this is what lets you visually verify the answer is actually grounded in the right slides.

- **`components/upload_ui.py`** — `render_upload(ingest_pdf_to_chroma)`. Sidebar widget that lets you upload PDF slides straight from the browser: saves them into `data/raw/` then calls the supplied ingestion function, which only processes the new/changed files thanks to the incremental ingestion manifest (see `src/README.md`).
