from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from retrieval.retriever import query_chroma
from generation.prompt_templates import build_prompt
from generation.llm_client import generate


def answer_question(question: str, top_k: int = 5) -> dict:
    chunks = query_chroma(question, top_k=top_k)
    prompt = build_prompt(question, chunks)
    answer = generate(prompt)
    return {"answer": answer, "chunks": chunks}


if __name__ == "__main__":
    result = answer_question("What is the difference between BFS and DFS?")
    print("ANSWER:", result["answer"])
    print("SOURCES:", [c["source"] for c in result["chunks"]])
