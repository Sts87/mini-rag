import json
from datetime import UTC, datetime
from pathlib import Path

from langchain_core.documents import Document

_LOG_DIR = Path(__file__).parent.parent / "data" / "logs"
_LOG_FILE = _LOG_DIR / "interactions.jsonl"


def log_interaction(
    query: str,
    results: list[tuple[Document, float]],
    answer: str,
    elapsed_seconds: float,
) -> None:
    """
    Appends a single interaction record to the JSONL log file.

    Each line is a self-contained JSON object with:
    - timestamp, query, answer, response_time_ms
    - retrieved documents (file_name, category, department, page, score)
    """
    _LOG_DIR.mkdir(parents=True, exist_ok=True)

    sources = [
        {
            "file_name": doc.metadata.get("file_name", "unknown"),
            "category": doc.metadata.get("category", "General"),
            "department": doc.metadata.get("department", "Desconocido"),
            "page": doc.metadata.get("page", "?"),
            "score": round(score, 4),
        }
        for doc, score in results
    ]

    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "query": query,
        "answer": answer,
        "response_time_ms": round(elapsed_seconds * 1000),
        "documents_retrieved": len(results),
        "sources": sources,
    }

    with open(_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
