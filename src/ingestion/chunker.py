"""Helpers for splitting loaded documents into smaller text chunks."""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pdf_document(docs):
    """Split documents into smaller chunks for embedding and retrieval.

    Uses a recursive splitter that prefers to break on paragraph/sentence/word
    boundaries before falling back to a hard character cut, and a larger
    chunk size so each chunk captures a coherent slide/section instead of an
    arbitrary 500-character slice.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=800,
        chunk_overlap=120,
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