import streamlit as st


def render_sources(chunks: list[dict]):
    """Render retrieved chunks in an expander so grounding can be checked visually."""
    with st.expander(f"Sources ({len(chunks)})"):
        for i, chunk in enumerate(chunks, 1):
            st.markdown(f"**[{i}] {chunk['source']}** — distance: {chunk['distance']:.4f}")
            st.text(chunk["document"][:500])
            st.divider()
