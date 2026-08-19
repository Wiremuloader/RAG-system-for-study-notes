import streamlit as st

from components.source_display import render_sources


def render_chat(answer_question):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("chunks"):
                render_sources(message["chunks"])

    question = st.chat_input("Ask a question about your lecture slides...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = answer_question(question)
            st.markdown(result["answer"])
            render_sources(result["chunks"])

        st.session_state.messages.append(
            {"role": "assistant", "content": result["answer"], "chunks": result["chunks"]}
        )
