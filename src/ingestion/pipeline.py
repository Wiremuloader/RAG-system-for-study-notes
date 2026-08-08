from sentence_transformers import SentenceTransformer
from loaders import load_pdf_document

def encode_sentences(sentences):
    # load a pretrained sentence transformer model
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # The sentences to encode 
    sentences = [doc.page_content for doc in load_pdf_document(None)]
    # encode the sentences
    embeddings = model.encode(sentences)
    return embeddings

if __name__ == "__main__":
    embeddings = encode_sentences(None)
    print(f"Embeddings shape: {embeddings.shape}")