import cohere
import faiss
import numpy as np
from langchain_core.documents import Document

from app.config import COHERE_API_KEY, EMBEDDING_MODEL, RETRIEVAL_TOP_K


def _embed_query(client: cohere.ClientV2, query: str) -> np.ndarray:
    response = client.embed(
        texts=[query],
        model=EMBEDDING_MODEL,
        input_type="search_query",
        embedding_types=["float"],
    )
    embeddings = response.embeddings.float_
    if embeddings is None:
        raise RuntimeError("Cohere did not return float embeddings.")
    return np.array(embeddings, dtype=np.float32)


def retrieve(
    query: str,
    index: faiss.IndexFlatIP,
    chunks: list[Document],
    k: int = RETRIEVAL_TOP_K,
) -> list[tuple[Document, float]]:
    """
    Returns the top-k most semantically similar chunks for a query,
    each paired with its cosine similarity score.
    """
    client = cohere.ClientV2(api_key=COHERE_API_KEY)

    query_vector = _embed_query(client, query)
    faiss.normalize_L2(query_vector)  # type: ignore[arg-type]

    scores, indices = index.search(query_vector, k)

    results: list[tuple[Document, float]] = []
    for score, idx in zip(scores[0], indices[0], strict=True):
        if idx == -1:
            continue
        results.append((chunks[idx], float(score)))

    return results
