from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from retrieval.retriever import query_chroma

questions = [
    "What is fuzzy logic control?",
    "How does the fuzzy inference engine work?",
    "What is the role of analog mode in the paper?"
]

for q in questions:
    print("\nQUESTION:", q)
    results = query_chroma(q, top_k=3)
    for i, item in enumerate(results, 1):
        print(f"{i}. distance={item['distance']:.4f}")
        print(item["document"][:400])
        print("-" * 80)