from langchain.embeddings import OpenAIEmbeddings

def get_embedding_model():
    return OpenAIEmbeddings(model="text-embedding-ada-002")