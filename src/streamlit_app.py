import time

import streamlit as st

from app.generator import generate
from app.indexer import load_index
from app.logger import log_interaction
from app.retriever import retrieve

st.set_page_config(
    page_title="Enterprise Knowledge AI",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Enterprise Knowledge AI")
st.caption("Asistente interno basado en documentos corporativos.")


@st.cache_resource(show_spinner="Cargando índice vectorial...")
def get_index():
    return load_index()


try:
    index, chunks = get_index()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

st.success(f"✓ Índice cargado — {len(chunks)} chunks de {index.ntotal} vectores.")

st.divider()

query = st.text_input(
    "¿Qué querés saber?",
    placeholder="Ej: ¿Cuál es el proceso de code review?",
)

if query:
    with st.spinner("Buscando en los documentos..."):
        start = time.perf_counter()
        results = retrieve(query, index, chunks)
        response = generate(query, results)
        elapsed = time.perf_counter() - start

        log_interaction(
            query=query,
            results=results,
            answer=response["answer"],
            elapsed_seconds=elapsed,
        )

    st.markdown("### Respuesta")
    st.write(response["answer"])

    if response["sources"]:
        with st.expander("📄 Fuentes utilizadas"):
            st.text(response["sources"])

    st.caption(f"⏱ Tiempo de respuesta: {elapsed * 1000:.0f} ms")
