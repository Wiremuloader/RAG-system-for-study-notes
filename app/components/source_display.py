import streamlit as st


def render_sources(chunks: list[dict]):
    """Render retrieved chunks in an expander so grounding can be checked visually."""
    with st.expander(f"Sources ({len(chunks)})"):
        for i, chunk in enumerate(chunks, 1):
            label = f"**[{i}] {chunk['source']}** — distance: {chunk['distance']:.4f}"
            if "rerank_score" in chunk:
                label += f" — rerank score: {chunk['rerank_score']:.4f}"
            st.markdown(label)
            st.text(chunk["document"][:500])
            st.divider()
