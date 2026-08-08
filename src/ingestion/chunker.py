"""Helpers for splitting loaded documents into smaller text chunks."""

from langchain_text_splitters import CharacterTextSplitter


def chunk_pdf_document(docs):
    """Split documents into smaller chunks for embedding and retrieval.

    The splitter uses a fixed-size character window with overlap so chunks
    remain manageable while preserving some surrounding context.
    """
    text_splitter = CharacterTextSplitter(
        separator="",
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False
    )

    chunks = text_splitter.split_documents(docs)

    print(f"Number of chunks created: {len(chunks)}")
    if chunks:
        print(chunks[0].page_content[:200])

    return chunks


if __name__ == "__main__":
    from ingestion.loaders import load_pdf_document

    docs = load_pdf_document(None)
    chunk_pdf_document(docs)