"""
Chunking methods:
fixed-size *
recursive chunking
semantic chunking
"""

from langchain_text_splitters import CharacterTextSplitter
from loaders import load_pdf_document

def chunk_pdf_document(docs):
    text_splitter = CharacterTextSplitter(
        separator="",
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False
    )

    chunks = text_splitter.split_documents(docs)
    
    print(f"Number of chunks created: {len(chunks)}")
    print(chunks[0].page_content)
    
if __name__ == "__main__":
    docs = load_pdf_document(None)
    chunk_pdf_document(docs)