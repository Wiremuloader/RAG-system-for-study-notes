import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.pipeline import ingest_pdf_to_chroma


def main():
    ingest_pdf_to_chroma()


if __name__ == "__main__":
    main()
