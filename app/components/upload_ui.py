from pathlib import Path

import streamlit as st

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def render_upload(ingest_pdf_to_chroma):
    """Sidebar widget: upload new lecture PDFs, save them to data/raw, and ingest just the new/changed files."""
    st.sidebar.header("Add lecture notes")
    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF slides", type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files and st.sidebar.button("Ingest uploaded files"):
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        for uploaded in uploaded_files:
            (RAW_DIR / uploaded.name).write_bytes(uploaded.getbuffer())

        with st.sidebar.status("Ingesting new/changed PDFs..."):
            # Rescans the whole raw folder; unchanged files are skipped, so this is cheap after the first run.
            ingest_pdf_to_chroma()

        st.sidebar.success(f"Ingested {len(uploaded_files)} uploaded file(s).")
