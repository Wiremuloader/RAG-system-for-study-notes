"""Utilities for loading PDF files into LangChain documents."""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_pdf_document(docs):
    """Load a PDF from the project data folder and return parsed documents.

    This uses PyPDFLoader with image extraction disabled because some scanned
    PDFs contain image streams that can break the parser.
    """
    pdf_path = Path("data/raw/Yamakawa_Fuzzy_Engine_Analog_Mode_Fuzzy_Logic_Control.pdf")

    # The source PDF contains scanned-page images encoded as CCITT fax data.
    # The image-extraction path in this parser can fail on those images, so we
    # disable image extraction and rely on plain text extraction from the PDF.
    loader = PyPDFLoader(
        file_path=str(pdf_path),
        mode="single",
        pages_delimiter=" ",
        extract_images=False,
    )

    docs = list(loader.lazy_load())

    if docs:
        print(docs[0].page_content[:100])
        print(docs[0].metadata)
    else:
        print("No documents were loaded.")
    return docs

if __name__ == "__main__":
    load_pdf_document(None)
    