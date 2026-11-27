import time
import streamlit as st

from app.generator import generate
from app.indexer import load_index
from app.logger import log_interaction
from app.retriever import retrieve

st.set_page_config(
    page_title="Enterprise Knowledge AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "font_size" not in st.session_state:
    st.session_state.font_size = "Normal"


def select_suggestion(text: str) -> None:
    st.session_state.pending_query = text


def clear_chat() -> None:
    st.session_state.messages = []
    st.session_state.pending_query = None


def format_elapsed(elapsed_ms: float) -> str:
    if elapsed_ms >= 1000:
        return f"{elapsed_ms / 1000:.2f} s"
    return f"{elapsed_ms:.0f} ms"


font_sizes = {
    "Pequeño": "0.92rem",
    "Normal": "1.05rem",
    "Grande": "1.2rem",
}
active_font_size = font_sizes.get(st.session_state.font_size, "1.05rem")

st.markdown(
    f"""
    <style>
        .block-container {{
            max-width: 920px;
            padding-top: 1.75rem;
            padding-bottom: 5rem;
        }}
        .app-header {{
            margin-bottom: 1rem;
        }}
        .app-subtitle {{
            color: #6b7280;
            font-size: 0.98rem;
            margin-top: -0.4rem;
        }}
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {{
            font-size: {active_font_size};
            line-height: 1.65;
        }}
        [data-testid="stChatMessage"] {{
            border-radius: 12px;
            padding: 0.35rem 0.6rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Cargando índice vectorial...")
def get_index():
    return load_index()


try:
    index, chunks = get_index()
except FileNotFoundError as e:
    st.error(f"No se pudo cargar el índice vectorial: {e}")
    st.stop()

with st.sidebar:
    st.header("⚙️ Estado del Sistema")
    st.success("Índice vectorial activo", icon="✅")

    col1, col2 = st.columns(2)
    col1.metric("Chunks", f"{len(chunks):,}")
    col2.metric("Vectores", f"{index.ntotal:,}")

    st.divider()
    st.subheader("🎨 Apariencia")
    st.select_slider(
        "Tamaño de texto",
        options=["Pequeño", "Normal", "Grande"],
        key="font_size",
    )

    st.divider()
    st.caption(f"Mensajes en sesión: {len(st.session_state.messages)}")
    st.button(
        "🗑️ Limpiar conversación",
        use_container_width=True,
        on_click=clear_chat,
        disabled=len(st.session_state.messages) == 0,
    )

st.markdown(
    """
    <div class="app-header">
        <h1>🤖 Enterprise Knowledge AI</h1>
        <p class="app-subtitle">Asistente interno basado en la documentación oficial de la empresa.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

suggestions = [
    "¿Cuál es el proceso de code review?",
    "¿Cómo solicito acceso a producción?",
    "Resumen de políticas de seguridad",
]

if not st.session_state.messages:
    st.markdown("**💡 Preguntas sugeridas para empezar:**")
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        cols[i].button(
            suggestion,
            key=f"sugg_{i}",
            use_container_width=True,
            on_click=select_suggestion,
            args=(suggestion,),
        )
    st.write("")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if msg.get("sources"):
                with st.expander("📄 Fuentes utilizadas"):
                    if isinstance(msg["sources"], list):
                        for src in msg["sources"]:
                            st.markdown(f"- {src}")
                    else:
                        st.markdown(str(msg["sources"]))
            if msg.get("elapsed_ms") is not None:
                st.caption(f"⏱ Tiempo de respuesta: {format_elapsed(msg['elapsed_ms'])}")

user_input = st.chat_input("Escribe tu consulta sobre la documentación interna...")

query = None
if user_input:
    query = user_input.strip()
elif st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None

if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.status("Analizando base de conocimiento...", expanded=False) as status:
            start = time.perf_counter()
            st.write("🔍 Recuperando fragmentos relevantes...")
            results = retrieve(query, index, chunks)

            st.write("🧠 Redactando respuesta...")
            response = generate(query, results)
            elapsed = time.perf_counter() - start
            elapsed_ms = elapsed * 1000

            status.update(
                label=f"Completado en {format_elapsed(elapsed_ms)}",
                state="complete",
            )

        answer_text = response["answer"]
        sources = response.get("sources")

        st.markdown(answer_text)

        if sources:
            with st.expander("📄 Fuentes utilizadas"):
                if isinstance(sources, list):
                    for src in sources:
                        st.markdown(f"- {src}")
                else:
                    st.markdown(str(sources))

        st.caption(f"⏱ Tiempo de respuesta: {format_elapsed(elapsed_ms)}")

        log_interaction(
            query=query,
            results=results,
            answer=answer_text,
            elapsed_seconds=elapsed,
        )

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer_text,
            "sources": sources,
            "elapsed_ms": elapsed_ms,
        }
    )