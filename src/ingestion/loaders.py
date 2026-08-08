from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

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