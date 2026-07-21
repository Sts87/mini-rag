# Enterprise Knowledge AI - Mini RAG

Enterprise AI Assistant powered by **Retrieval-Augmented Generation (RAG)**, designed to answer questions from internal corporate documentation with **semantic search, contextual generation, and source citations**.

Built for **Santo Pegasus Soluciones**.

---

# Features

- Answer questions from internal corporate documentation
- Semantic search using multilingual embeddings
- Retrieval-Augmented Generation (RAG)
- Source citations for generated responses
- PDF document ingestion and chunking
- Persistent FAISS vector index
- JSONL interaction logging
- Streamlit web interface
- Containerized deployment with Podman
- Infrastructure as Code with Terraform
- CI/CD automation with GitHub Actions
- Deployment on Oracle Cloud Infrastructure (OCI)

---

# Architecture

## Indexing Pipeline

```text
PDF Documents
      │
      ▼
    Loader
      │
      ▼
   Chunker
      │
      ▼
Cohere Embeddings
      │
      ▼
 FAISS Index
      │
      ▼
Persistent Vector Store
```

## Query Pipeline

```text
User Query
      │
      ▼
Cohere Embeddings
      │
      ▼
Semantic Search
      │
      ▼
Relevant Documents
      │
      ▼
Cohere Chat
      │
      ▼
Answer + Source Citations
```

---

# Tech Stack

| Layer | Technology |
|--------|------------|
| Embeddings | Cohere embed-multilingual-v3.0 |
| Vector Store | FAISS IndexFlatIP (cosine similarity) |
| LLM | Cohere command-r-plus-08-2024 |
| Interface | Streamlit |
| Containerization | Podman + podman-compose |
| Cloud Infrastructure | Oracle Cloud Infrastructure (OCI) |
| Infrastructure as Code | Terraform |
| CI/CD | GitHub Actions |
| Python | 3.12+ |
| Package Manager | uv |

---

# Project Structure

```text
mini-rag/
├── src/
│   ├── app/
│   │   ├── config.py              # Application settings from .env
│   │   ├── loader.py              # PDF loading and metadata extraction
│   │   ├── chunker.py             # Document chunking
│   │   ├── indexer.py             # Embeddings + FAISS index management
│   │   ├── retriever.py           # Semantic document retrieval
│   │   ├── generator.py           # Prompt construction + Cohere Chat
│   │   └── logger.py              # JSONL interaction logging
│   │
│   ├── scripts/
│   │   └── build_index.py         # Builds the vector index
│   │
│   └── streamlit_app.py           # Streamlit web interface
│
├── data/
│   ├── documents/                 # Corporate PDF documents
│   ├── vectorstore/               # Persisted FAISS index
│   └── logs/                      # Application interaction logs
│
├── infrastructure/                # Terraform configuration for OCI
├── compose.yml                    # Local development environment
├── compose.prod.yml               # Production environment
├── Dockerfile                     # Multi-stage container build
├── Makefile                       # Development and deployment commands
└── .github/
    └── workflows/                 # CI/CD pipelines
```

---

# Local Setup

## Requirements

- Python 3.12+
- uv
- Podman
- podman-compose
- Cohere API Key

---

## 1. Clone the Repository

```bash
git clone <repo>
cd mini-rag
```

---

## 2. Install Dependencies

```bash
uv sync
```

---

## 3. Configure Environment Variables

```bash
cp .env.example .env
```

Add your API key:

```env
COHERE_API_KEY=your_api_key
```

---

# Add Documents

Place your corporate PDF files inside:

```text
data/documents/
```

Each document may include metadata such as:

- Category
- Department
- File name
- Page number

---

# Build the Vector Index

Generate the FAISS index:

```bash
uv run python src/scripts/build_index.py
```

The resulting vector database is stored in:

```text
data/vectorstore/
```

---

# Run the Application

## Development

```bash
uv run streamlit run src/streamlit_app.py
```

## Containerized

```bash
make build
make index
make run
```

Application URL:

```text
http://localhost:8501
```

---

# Deployment on Oracle Cloud Infrastructure

The application can be deployed on an OCI Virtual Machine using Terraform and Podman.

---

## Provision Infrastructure

```bash
cd infrastructure/

terraform init
terraform plan
terraform apply
```

---

## Manual Deployment

Build and export the image:

```bash
podman save mini-rag:latest -o mini-rag.tar
```

Copy the required files:

```bash
scp -i ~/.ssh/<key> \
  mini-rag.tar \
  compose.prod.yml \
  .env \
  opc@<IP>:/opt/mini-rag/
```

Load and start the application:

```bash
podman load -i mini-rag.tar

podman-compose -f compose.prod.yml up -d
```

---

# CI/CD

Every push to the **main** branch triggers:

```text
Lint (Ruff)
    │
    ▼
Build Container
    │
    ▼
Transfer Image to OCI VM
    │
    ▼
Deploy
    │
    ▼
Health Check
```

---

## Required GitHub Secrets

| Secret | Description |
|---------|-------------|
| VM_HOST | Public IP of the OCI VM |
| VM_USER | SSH user (typically `opc`) |
| VM_KEY | SSH private key |
| COHERE_API_KEY | Cohere API key |

---

# Indexed Documents

| File | Category | Department |
|------|----------|------------|
| manual_onboarding.pdf | RRHH | People & Engineering |
| guia_oficial_ingenieria_backend.pdf | Engineering | Chapter de Back-end |
| guia_oficial_ingenieria_frontend.pdf | Engineering | Chapter de Front-end |
| arquitectura_de_microservicios_y_mapa_de_dominios.pdf | Architecture | Chapter de Back-end |
| protocolo_respuesta_incidentes_y_post_mortems.pdf | Operations | Chapter de SRE |

---

# Observability & Logging

Each interaction is stored in:

```text
data/logs/interactions.jsonl
```

Example:

```json
{
  "timestamp": "2026-07-19T23:45:12+00:00",
  "query": "¿Cómo se hace un code review?",
  "answer": "...",
  "response_time_ms": 1823,
  "documents_retrieved": 5,
  "sources": [
    {
      "file_name": "manual_onboarding.pdf",
      "category": "RRHH",
      "department": "People & Engineering",
      "page": 12,
      "score": 0.6721
    }
  ]
}
```

The logs provide traceability for:

- User queries
- Generated responses
- Response latency
- Number of retrieved documents
- Source documents
- Document categories
- Departments
- Retrieval similarity scores

---

# End-to-End Flow

```text
                    ┌─────────────────────┐
                    │  Corporate PDFs     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Document Loader    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Chunker        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Cohere Embeddings   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FAISS Vector DB   │
                    └──────────┬──────────┘
                               │
                               │
                     User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Query Embedding     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Semantic Retrieval  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Cohere Chat      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Answer + Citations  │
                    └─────────────────────┘
```

---

# Infrastructure

```text
Developer
    │
    │ git push
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Lint
    ├── Build
    ├── Transfer
    └── Deploy
           │
           ▼
Oracle Cloud Infrastructure
           │
           ▼
      OCI Virtual Machine
           │
           ▼
     Podman Container
           │
           ▼
    Streamlit Application
```

---

# Project Goals

This project demonstrates the implementation of a production-oriented **Retrieval-Augmented Generation (RAG)** pipeline by combining:

- LLM-powered knowledge retrieval
- Semantic search
- Vector indexing
- Document processing
- Containerization
- Infrastructure as Code
- Cloud deployment
- Automated CI/CD
- Interaction logging and traceability

The architecture is designed to provide a reproducible and automated deployment workflow from local development to cloud infrastructure.