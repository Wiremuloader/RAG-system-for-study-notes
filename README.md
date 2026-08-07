# RAG-system-for-study-notes
Implementing a RAG system on lectures and workshops to help with uni study (open-source)

Planning - on GitHub
Components of the system:
Document loading and chunking

Embedding model

vector database

llm for generation

orchestration

interface

Basic architecture:
ingest documents
chunk the text into manageable pieces
embed those chunks into a vectors
store the vectors in a vector database
retrieve relevant chunks based when a query is made
generate an answer using an llm, grounded in those retrieved chunks
