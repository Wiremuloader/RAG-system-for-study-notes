from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from retrieval.retriever import query_chroma

questions = [
    "What is the difference between BFS and DFS?",
    "How does A* search use heuristics?",
    "What is uniform-cost search?",
]

for q in questions:
    print("\nQUESTION:", q)
    results = query_chroma(q, top_k=3, use_reranker=True)
    for i, item in enumerate(results, 1):
        print(f"{i}. distance={item['distance']:.4f} rerank_score={item['rerank_score']:.4f} source={item['source']}")
        print(item["document"][:400])
        print("-" * 80)