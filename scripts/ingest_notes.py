import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.pipeline import ingest_pdf_to_chroma


def main():
    parser = argparse.ArgumentParser(description="Batch-ingest lecture note PDFs into Chroma.")
    parser.add_argument(
        "--source",
        default=None,
        help="Folder of PDFs or a single PDF file to ingest (default: data/raw)",
    )
    parser.add_argument("--collection", default="study-notes", help="Chroma collection name")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-ingest files even if unchanged since the last run",
    )
    args = parser.parse_args()

    ingest_pdf_to_chroma(source=args.source, collection_name=args.collection, force=args.force)


if __name__ == "__main__":
    main()
