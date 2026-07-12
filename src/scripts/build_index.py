from app.chunker import split_documents
from app.config import DOCUMENTS_DIR
from app.indexer import build_index
from app.loader import load_pdfs


def main() -> None:
    print("=" * 52)
    print("Enterprise Knowledge AI — Build Index")
    print("=" * 52)

    print("\n[1/3] Cargando PDFs...")
    documents = load_pdfs(DOCUMENTS_DIR)
    print(f"  Total páginas cargadas: {len(documents)}")

    print("\n[2/3] Dividiendo en chunks...")
    chunks = split_documents(documents)
    print(f"  Total chunks generados: {len(chunks)}")

    print("\n[3/3] Generando embeddings e indexando...")
    build_index(chunks)

    print("\n✓ Índice construido exitosamente.")


if __name__ == "__main__":
    main()
