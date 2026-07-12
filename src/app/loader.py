from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdfs(directory: str | Path) -> list[Document]:
    """
    Loads all PDFs from a directory.
    Each page becomes a Document with metadata: source, page, file_name.
    """
    directory = Path(directory)
    documents: list[Document] = []

    pdf_files = sorted(directory.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {directory}")

    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()

        for page in pages:
            page.metadata["file_name"] = pdf_path.name

        documents.extend(pages)
        print(f"  Loaded: {pdf_path.name} ({len(pages)} pages)")

    return documents
