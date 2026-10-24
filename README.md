# zerTrace

zerTrace is an AI-powered contributor assistant that helps developers and newcomers understand open-source repositories, onboarding docs, and contribution guides using a document-grounded RAG workflow.

The application allows users to upload documentation, ask questions in natural language, and receive beginner-friendly answers backed by relevant source excerpts from the uploaded material.

---

## Overview

When working with large open-source projects, new contributors often struggle to find the right documentation, understand the project structure, and determine where to begin. zerTrace solves this by turning project docs into a searchable knowledge base.

Users can:
- upload contribution guides, READMEs, or documentation files
- ask questions such as "How do I start contributing?"
- receive a grounded answer based on the uploaded material
- inspect the source sections that informed the response

---

## Problem it solves

Open-source repositories usually contain scattered knowledge across:
- README files
- contribution guides
- setup instructions
- architecture notes
- issue templates and governance docs

This project makes that information accessible through a conversational interface, reducing the time needed to understand a project before contributing.

---

## Key features

- Intelligent document ingestion for PDF, Markdown, and text files
- Text chunking and indexing for retrieval
- Embedding-based semantic search
- Keyword + vector hybrid retrieval
- Relevance filtering before answer generation
- LLM-based answer generation grounded in retrieved evidence
- Citation tracking to source documents
- Modern web frontend for file upload and Q&A
- Lightweight local development setup

---

## Architecture

The repository follows a simple but effective RAG pipeline:

1. User uploads a document
2. Backend stores the file locally
3. Content is extracted and cleaned
4. Text is split into chunks
5. Chunks are embedded and stored in ChromaDB
6. User asks a question
7. Backend retrieves the best matching chunks
8. A model generates an answer using only the relevant evidence
9. The frontend presents the answer and sources

### High-level flow

Client (React UI)
  -> FastAPI backend
      -> document loader and chunker
      -> embeddings + vector store
      -> hybrid retrieval
      -> relevance check
      -> LLM answer generation
      -> citations returned to frontend

---

## Repository structure

```text
zerTrace/
├── README.md
├── .gitignore
├── 02_rag_starter_kit.ipynb
├── colab_setup.ipynb
├── demo-contribution-guide.md
├── demo-contribution-guide.txt
├── backend/
│   ├── .env.example
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── data/
│   ├── tests/
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── api/
│       │   ├── chat.py
│       │   ├── documents.py
│       │   ├── onboarding.py
│       │   └── evaluation.py
│       ├── rag/
│       │   ├── chunker.py
│       │   ├── citations.py
│       │   ├── embeddings.py
│       │   ├── generator.py
│       │   ├── hybrid_retriever.py
│       │   ├── keyword_retriever.py
│       │   ├── loader.py
│       │   ├── pipeline.py
│       │   ├── relevance_gate.py
│       │   ├── reranker.py
│       │   └── vector_store.py
│       └── services/
├── frontend/
│   ├── index.html
│   ├── netlify.toml
│   ├── package.json
│   ├── package-lock.json
│   └── src/
│       ├── App.tsx
│       └── main.tsx
└── ...
```

---

## Tech stack

### Backend
- Python
- FastAPI
- ChromaDB
- Pydantic Settings
- sentence-transformers / embedding models
- Gemini / Gemma-style model integration
- pytest

### Frontend
- React
- TypeScript
- Vite
- CSS-in-JS styling

---

## Backend modules

### API layer
The backend is registered in `backend/app/main.py` and contains the main API routes.

Core routes:
- `/api/health` – health check and backend status
- `/api/documents/upload` – upload and index documents
- `/api/documents` – list indexed docs
- `/api/documents/{doc_id}` – delete a document
- `/api/chat` – ask a question about indexed content
- `/api/onboarding` – provide contributor guidance
- `/api/evaluation` – evaluation endpoints

### RAG pipeline
The retrieval and answer generation flow is implemented under `backend/app/rag/`:

- `loader.py` – loads documents and normalizes text
- `chunker.py` – splits document text into chunks
- `embeddings.py` – creates embeddings for queries and documents
- `vector_store.py` – stores and queries vector data in Chroma
- `keyword_retriever.py` – performs keyword-based matching
- `hybrid_retriever.py` – combines recall from both semantic and keyword searches
- `relevance_gate.py` – filters weak or irrelevant matches
- `generator.py` – produces the final model output
- `citations.py` – validates citations against source chunks
- `pipeline.py` – orchestrates the entire retrieval-generation flow

---

## Frontend experience

The frontend is a chat-style application built with React and Vite.

It enables users to:
- select a file for upload
- send natural-language questions
- get AI-generated answers
- view references and evidence
- trigger starter guidance for onboarding questions
- switch between light and dark mode

The frontend communicates with the backend at `http://localhost:8000` by default.

---

## Environment configuration

The backend configuration is managed through `backend/app/config.py` and the example environment file `backend/.env.example`.

Example variables:

```env
GOOGLE_API_KEY=
GEMMA_MODEL=gemma-2-9b-it
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIRECTORY=./data/chroma
UPLOAD_DIRECTORY=./data/uploads
CHUNK_SIZE=800
CHUNK_OVERLAP=150
TOP_K=5
RELEVANCE_THRESHOLD=0.25
ENABLE_RERANKER=false
FRONTEND_ORIGIN=http://localhost:5173
```

---

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/hemanth1127-code/zerTrace.git
cd zerTrace
```

### 2. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# set GOOGLE_API_KEY in .env
uvicorn app.main:app --reload --port 8000
```

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend typically runs at:
- `http://localhost:5173`

---

## Typical workflow

1. Open the frontend in the browser
2. Upload a project guide or contribution document
3. Wait for the backend to process the file and index it
4. Ask a question like:
   - "How do I start contributing?"
   - "Which files should I inspect before creating a PR?"
   - "What is the expected contribution workflow?"
5. The backend retrieves the relevant document chunks
6. The model generates a concise and grounded answer
7. The UI displays the answer and source references

---

## Example request flow

### Chat request

```json
{
  "question": "How should a beginner contribute to this project?",
  "mode": "hybrid",
  "top_k": 5
}
```

### Backend behavior
- embed the question
- search the vector store
- combine with keyword retrieval
- run relevance checks
- generate a response using the best evidence
- return citations and the answer payload

---

## Why this project is useful

zerTrace is especially useful for:
- onboarding new contributors
- helping first-time developers understand docs faster
- turning static documentation into interactive knowledge
- building internal contributor assistant tools for open-source repositories

---

## Potential improvements

Some natural next steps include:
- support for more file types like DOCX, HTML, and PPTX
- multi-user / per-project indexing
- GitHub repository metadata integration
- stronger citation validation
- persistent deployment setup for production use
- authentication and user-specific document libraries

---

## Testing

The backend includes a test folder and can be run with:

```bash
cd backend
pytest
```

---

## Deployment considerations

This project is set up for local development and demonstration, but it can be adapted for production with:
- frontend hosting on Netlify or Vercel
- backend deployment on Render, Railway, Azure, or Docker
- secure environment management for API keys
- persistent storage for uploaded documents and Chroma data

---

## Summary

zerTrace combines a modern frontend, FastAPI backend, and retrieval-augmented generation pipeline to help users understand project documentation and contributions more efficiently. It is a practical AI assistant for onboarding, documentation navigation, and contributor support in open-source environments.

---

## Quick start

```bash
# backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add GOOGLE_API_KEY
uvicorn app.main:app --reload --port 8000

# frontend
cd ../frontend
npm install
npm run dev
```

Then open the frontend and upload a guide or project document to start asking questions.

---

## Project link

- GitHub: https://github.com/hemanth1127-code/zerTrace
