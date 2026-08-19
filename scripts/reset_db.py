import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.pipeline import MANIFEST_PATH
from src.vectorStore.chroma_client import get_collection


def main():
    get_collection("study-notes", recreate=True)
    if MANIFEST_PATH.exists():
        MANIFEST_PATH.unlink()
    print("Cleared the 'study-notes' collection and ingestion manifest.")


if __name__ == "__main__":
    main()
