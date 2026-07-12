from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

_DOCUMENT_CATALOG: dict[str, dict[str, str]] = {
    "manual_onboarding.pdf": {
        "category": "RRHH",
        "department": "People & Engineering",
        "version": "1.0.0",
    },
    "guia_oficial_ingenieria_backend.pdf": {
        "category": "Engineering",
        "department": "Chapter de Back-end",
        "version": "2.4.0",
    },
    "guia_oficial_ingenieria_frontend.pdf": {
        "category": "Engineering",
        "department": "Chapter de Front-end",
        "version": "1.0.0",
    },
    "arquitectura_de_microservicios_y_mapa_de_dominios.pdf": {
        "category": "Architecture",
        "department": "Chapter de Back-end",
        "version": "1.0.0",
    },
    "protocolo_respuesta_incidentes_y_post_mortems.pdf": {
        "category": "Operations",
        "department": "Chapter de SRE",
        "version": "1.0.0",
    },
}

def load_pdfs(directory: str | Path) -> list[Document]:
    """
    Loads all PDFs from a directory.
    Each page becomes a Document enriched with: file_name, category,
    department and version from the document catalog.
    """
    directory = Path(directory)
    documents: list[Document] = []

    pdf_files = sorted(directory.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {directory}")

    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()

        catalog_entry = _DOCUMENT_CATALOG.get(pdf_path.name, {})

        for page in pages:
            page.metadata["file_name"] = pdf_path.name
            page.metadata["category"] = catalog_entry.get("category", "General")
            page.metadata["department"] = catalog_entry.get("department", "Desconocido")
            page.metadata["version"] = catalog_entry.get("version", "?")

        documents.extend(pages)
        category = catalog_entry.get("category", "General")
        print(f"  Loaded: {pdf_path.name} ({len(pages)} pages) [{category}]")

    return documents
