def build_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    context_blocks = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        source = chunk.get("source", "unknown")
        context_blocks.append(f"[{i}] (source: {source})\n{chunk['document']}")

    context = "\n\n".join(context_blocks)

    return (
        "You are a study assistant answering questions about lecture slides.\n"
        "Use ONLY the context below to answer the question. "
        "If the answer is not contained in the context, say you don't know "
        "instead of guessing.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )
