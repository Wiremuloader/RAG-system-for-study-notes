from vectorStore.chroma_client import client, get_collection
from retrieval.retriever import model, query_chroma

TEST_COLLECTION = "test-retrieval-smoke"


def test_query_chroma_returns_most_similar_chunk():
    collection = get_collection(TEST_COLLECTION, recreate=True)

    documents = [
        "Breadth-first search explores nodes level by level using a queue.",
        "A* search combines path cost with a heuristic estimate to the goal.",
        "Uniform-cost search expands the node with the lowest cumulative path cost.",
    ]
    embeddings = model.encode(documents, normalize_embeddings=True)

    collection.upsert(
        ids=[f"doc-{i}" for i in range(len(documents))],
        embeddings=embeddings.tolist(),
        documents=documents,
        metadatas=[{"source": "smoke-test.pdf"} for _ in documents],
    )

    try:
        results = query_chroma("How does BFS explore a graph?", top_k=1, collection_name=TEST_COLLECTION)

        assert len(results) == 1
        assert "queue" in results[0]["document"].lower()
        assert results[0]["source"] == "smoke-test.pdf"
    finally:
        client.delete_collection(TEST_COLLECTION)
