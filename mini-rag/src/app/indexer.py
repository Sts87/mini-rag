import pickle

import cohere
import faiss
import numpy as np
from langchain_core.documents import Document

from app.config import (
    COHERE_API_KEY,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    VECTORSTORE_DIR,
)

_INDEX_FILE = VECTORSTORE_DIR / "index.faiss"
_CHUNKS_FILE = VECTORSTORE_DIR / "chunks.pkl"
_BATCH_SIZE = 90


def _get_client() -> cohere.ClientV2:
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY not set. Check your .env file.")
    return cohere.ClientV2(api_key=COHERE_API_KEY)


def _embed(
    client: cohere.ClientV2,
    texts: list[str],
    input_type: str,
) -> np.ndarray:
    all_embeddings: list[list[float]] = []

    for i in range(0, len(texts), _BATCH_SIZE):
        batch = texts[i : i + _BATCH_SIZE]
        print(
            f"    Batch {i // _BATCH_SIZE + 1}/{-(-len(texts) // _BATCH_SIZE)}"
            f" ({len(batch)} chunks)..."
        )

        response = client.embed(
            texts=batch,
            model=EMBEDDING_MODEL,
            input_type=input_type,
            embedding_types=["float"],
        )
        embeddings = response.embeddings.float_
        if embeddings is None:
            raise RuntimeError("Cohere did not return float embeddings.")
        all_embeddings.extend(embeddings)

    return np.array(all_embeddings, dtype=np.float32)


def build_index(chunks: list[Document]) -> None:
    """
    Embeds all chunks in batches and saves the FAISS index + chunks to disk.
    """
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    client = _get_client()
    texts = [chunk.page_content for chunk in chunks]

    print(f"  Embedding {len(texts)} chunks with Cohere...")
    vectors = _embed(client, texts, input_type="search_document")

    faiss.normalize_L2(vectors)  # type: ignore[arg-type]

    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(vectors)

    faiss.write_index(index, str(_INDEX_FILE))

    with open(_CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"  Index saved: {index.ntotal} vectors → {VECTORSTORE_DIR}")


def load_index() -> tuple[faiss.IndexFlatIP, list[Document]]:
    """
    Loads the FAISS index and chunk list from disk.
    """
    if not _INDEX_FILE.exists() or not _CHUNKS_FILE.exists():
        raise FileNotFoundError(
            "Vector store not found. Run scripts/build_index.py first."
        )

    index = faiss.read_index(str(_INDEX_FILE))

    with open(_CHUNKS_FILE, "rb") as f:
        chunks: list[Document] = pickle.load(f)

    return index, chunks  # type: ignore[return-value]
