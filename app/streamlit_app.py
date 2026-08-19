from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src", ROOT / "app"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generation.rag_chain import answer_question
from ingestion.pipeline import ingest_pdf_to_chroma
from components.chat_ui import render_chat
from components.upload_ui import render_upload

st.set_page_config(page_title="Study Notes RAG", page_icon="📚")
st.title("📚 Study Notes RAG")

render_upload(ingest_pdf_to_chroma)
render_chat(answer_question)
