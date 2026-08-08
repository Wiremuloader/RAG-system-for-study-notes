# RAG-system-for-study-notes
Implementing a RAG system on lectures and workshops to help with uni study (open-source)

Problem: I have too many lecture slides to study and not enough time to sift through them all let alone study them. I want to be able to ask questions and get answers based on the courses content

## Planning - on GitHub
Components of the system:
Document loading and chunking
Embedding model
vector database
llm for generation
orchestration
interface


## Basic architecture:
Ingest documents
Chunk the text into manageable pieces
Embed those chunks into vectors
Store the vectors in a vector database
Retrieve relevant chunks based on when a query is made
Generate an answer using an llm, grounded in those retrieved chunks


