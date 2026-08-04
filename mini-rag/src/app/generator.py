import cohere
from cohere.types import SystemChatMessageV2, UserChatMessageV2
from langchain_core.documents import Document

from app.config import CHAT_MODEL, COHERE_API_KEY

SYSTEM_PROMPT = (
    "Eres un asistente interno de Santo Pegasus Soluciones, empresa especializada en "
    "desarrollo de software escalable bajo arquitectura de microservicios e "
    "Inteligencia Artificial. Respondes preguntas de los colaboradores "
    "basándote EXCLUSIVAMENTE en los documentos internos proporcionados.\n\n"
    "Reglas:\n"
    "- Responde solo con información presente en el contexto. "
    "No uses conocimiento externo.\n"
    "- Si la información no está en el contexto, responde exactamente: "
    '"No encontré información sobre eso en los documentos disponibles."\n'
    "- Sé claro, directo y conciso.\n"
    "- Responde siempre en español."
)

FALLBACK = "No encontré información sobre eso en los documentos disponibles."

def build_context(results: list[tuple[Document, float]]) -> str:
    parts: list[str] = []

    for doc, score in results:
        file_name = doc.metadata.get("file_name", "Desconocido")
        category = doc.metadata.get("category", "General")
        department = doc.metadata.get("department", "Desconocido")
        page = doc.metadata.get("page", "?")

        parts.append(
            f"[Fuente: {file_name} | {category} — {department} | "
            f"Página {page} | Relevancia: {score:.2f}]\n"
            f"{doc.page_content}"
        )

    return "\n\n---\n\n".join(parts)

def generate(
    query: str,
    results: list[tuple[Document, float]],
) -> dict[str, str]:
    """
    Generates a response grounded in the retrieved chunks.
    Returns a dict with 'answer' and 'sources'.
    """
    if not results:
        return {"answer": FALLBACK, "sources": ""}

    context = build_context(results)

    user_message = (
        f"Contexto de documentos internos:\n\n{context}\n\n---\n\n"
        f"Pregunta del colaborador: {query}"
    )

    client = cohere.ClientV2(api_key=COHERE_API_KEY)

    response = client.chat(
        model=CHAT_MODEL,
        messages=[
            SystemChatMessageV2(content=SYSTEM_PROMPT),
            UserChatMessageV2(content=user_message),
        ],
    )

    content_items = response.message.content

    if content_items and len(content_items) > 0:
        answer = getattr(content_items[0], "text", "")
    else:
        answer = FALLBACK

    sources = _format_sources(results)

    return {"answer": answer, "sources": sources}

def _format_sources(results: list[tuple[Document, float]]) -> str:
    seen: set[str] = set()
    lines: list[str] = []

    for doc, score in results:
        file_name = doc.metadata.get("file_name", "Desconocido")
        category = doc.metadata.get("category", "General")
        department = doc.metadata.get("department", "Desconocido")
        page = doc.metadata.get("page", "?")
        key = f"{file_name}-{page}"

        if key not in seen:
            seen.add(key)
            lines.append(
                f"• {file_name} — {category} | {department} "
                f"| Página {page} (relevancia: {score:.2f})"
            )

    return "\n".join(lines)
