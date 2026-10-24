# zerTrace / ContribGuide AI

A full-stack AI assistant built to help new contributors understand open-source projects, onboarding docs, and contribution guides. The project combines a FastAPI backend, a React frontend, and a retrieval-augmented generation (RAG) pipeline that answers questions from uploaded documentation while grounding the response in source excerpts.

This repository is designed for the following use case:
- A contributor uploads project docs or contribution guides
- The app chunks and indexes the content
- The system retrieves the most relevant sections for a user question
- A language model generates a beginner-friendly answer with citations
- The frontend shows the answer and source references in a chat-like interface

---

## Why this project exists

New contributors often struggle to find the right place to start in large open-source repositories. Documentation is usually scattered across README files, contribution guides, setup instructions, and project-specific notes. This project reduces that friction by turning documentation into a searchable, guided knowledge assistant.

Instead of forcing contributors to read long documents manually, the app helps them ask specific questions such as:
- Where should I start contributing?
- How do I set up the project locally?
- What is the expected contribution workflow?
- Which docs explain the repo architecture or contribution process?

---

## Project overview

The system has two main layers:

1. Backend (Python + FastAPI)
   - Handles document upload and indexing
   - Stores chunks in a vector database
   - Retrieves relevant content using hybrid search
   - Calls the LLM to generate answers grounded in document evidence

2. Frontend (React + Vite)
   - Uploads documents
   - Lets users ask questions in a chat interface
   - Displays AI responses and source snippets

---

## Architecture

The repository follows a lightweight RAG architecture:

Client (React UI)
  -> FastAPI endpoints
      -> Document loader / chunker
      -> Embedding generation
      -> Chroma vector store
      -> Hybrid retrieval (keyword + semantic)
      -> Relevance filter
      -> LLM answer generation
      -> Citations and evidence returned to UI

Core logic flow:
- Uploaded files are validated (.pdf, .md, .txt)
- Text is extracted and cleaned
- The content is split into chunks
- Each chunk gets an embedding
- Relevant chunks are retrieved using query embedding and keyword matching
- The app generates a response using only relevant context
- Citations are checked to ensure the answer stays grounded in document evidence

---

## Tech stack

Backend
- Python 3.10+
- FastAPI
- ChromaDB
- sentence-transformers / embeddings
- Google Gemini / Gemma-based inference
- Pydantic settings
- pytest

Frontend
- React
- TypeScript
- Vite
- CSS-in-JS styling

Additional components
- PDF/text document parsing
- Hybrid retrieval using vector + keyword search
- Local file storage for uploads

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
│           └── ...
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

## Backend details

### API entry point
The backend is launched via `backend/app/main.py`.

Main endpoints:
- `/api/health` - health check for backend and vector store status
- `/api/documents/upload` - upload and index a `.pdf`, `.md`, or `.txt` file
- `/api/documents` - list indexed docs metadata
- `/api/documents/{doc_id}` - delete a document by source name
- `/api/chat` - ask a question against indexed docs
- `/api/onboarding` - return onboarding guidance steps
- `/api/evaluation` - evaluation-related endpoints

### Config
The backend uses environment variables defined in `backend/.env.example` and loaded from `.env` through `pydantic-settings`.

Key settings:
- `GOOGLE_API_KEY` - required for model access
- `GEMMA_MODEL` - selected model for generation
- `EMBEDDING_MODEL` - embedding model for document/query encoding
- `CHROMA_PERSIST_DIRECTORY` - vector database storage path
- `UPLOAD_DIRECTORY` - local location for uploaded files
- `CHUNK_SIZE` and `CHUNK_OVERLAP` - splitting configuration
- `TOP_K` - number of relevant chunks to retrieve
- `RELEVANCE_THRESHOLD` - cutoff for answer eligibility
- `FRONTEND_ORIGIN` - CORS origin for frontend access

---

## Frontend details

The frontend is a single-page React app built with Vite.

Main UI behavior:
- Choose a file and upload documentation
- Ask open questions to the AI assistant
- Get answer and source references
- Ask onboarding questions like "Where do I start?"
- Toggle between light and dark mode

The app calls the backend at `http://localhost:8000` by default.

---

## Detailed workflow

### 1. Setup and environment preparation
Before running the app:
- Create a Python virtual environment for the backend
- Install backend requirements
- Create `.env` from `.env.example`
- Add your Google API key
- Install frontend dependencies

### 2. Start backend
Run:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# set GOOGLE_API_KEY in .env
uvicorn app.main:app --reload --port 8000
```

This starts the FastAPI API server.

### 3. Start frontend
Run in a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend becomes available via the Vite dev server, usually on:
- `http://localhost:5173`

### 4. Upload documentation
From the UI:
- Select a file (`.pdf`, `.md`, or `.txt`)
- Click "Upload Doc"

The backend performs the following:
- saves the file under `backend/data/uploads`
- validates the size and extension
- loads and extracts text
- splits the text into chunks
- embeds the chunks
- inserts them into ChromaDB

### 5. Ask a question
The frontend sends a POST request to:

```http
POST /api/chat
```

with a payload such as:

```json
{
  "question": "How do I get started contributing to this project?",
  "mode": "hybrid",
  "top_k": 5
}
```

### 6. Backend retrieval and generation
The backend does the following:
- embeds the incoming question
- retrieves candidate chunks from the vector store
- performs keyword-based matching for better recall
- applies a relevance gate to decide if the evidence is strong enough
- sends the filtered evidence to the LLM
- validates that generated citations are consistent with retrieved chunks
- returns the final answer and citations to the UI

### 7. Response shown to the user
The frontend displays:
- the AI answer text
- the relevant source names
- the retrieved document evidence (if available)

---

## RAG pipeline internals

The retrieval pipeline is spread across several modules:

- `loader.py` - loads document content and normalizes text
- `chunker.py` - splits documents into manageable chunks
- `embeddings.py` - converts text into embeddings
- `vector_store.py` - manages ChromaDB indexing and retrieval
- `keyword_retriever.py` - supports keyword-based retrieval
- `hybrid_retriever.py` - combines semantic and lexical search
- `relevance_gate.py` - checks whether retrieved content is relevant enough
- `generator.py` - builds the final answer from retrieved context
- `citations.py` - ensures answer claims map to valid evidence
- `pipeline.py` - orchestrates the end-to-end retrieval and generation flow

This is a classic RAG approach:
- retrieval: find the most relevant documentation segments
- grounding: use only retrieved evidence
- generation: write answer based on that context
- verification: confirm citations map back to the source material

---

## Example flow

A typical user session looks like this:

1. User uploads `CONTRIBUTING.md`
2. Backend extracts and chunks the file
3. Chunks are embedded and saved in the database
4. User asks: "Which files should I inspect before opening a PR?"
5. The app searches relevant chunks
6. The model answers using the retrieved sections from the docs
7. The frontend shows the answer with source references

---

## Local development commands

Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Frontend

```bash
cd frontend
npm install
npm run dev
```

Tests

```bash
cd backend
pytest
```

Build frontend

```bash
cd frontend
npm run build
```

---

## Common environment variables

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

## Deployment thoughts

This project is currently structured for local development and demo usage. In production, a typical deployment pattern would be:

- Frontend: static hosting such as Netlify or Vercel
- Backend: FastAPI service hosted on Render, Railway, Azure, or a Docker container
- Vector DB: persistent Chroma storage or managed equivalent
- Secrets: store `GOOGLE_API_KEY` in a secure environment system
- File uploads: persist to object storage or a dedicated uploads service in production

---

## Troubleshooting

### Backend fails to start
- Check that `.env` exists in `backend/`
- Confirm your `GOOGLE_API_KEY` is set
- Install all Python dependencies from `requirements.txt`

### Frontend cannot call backend
- Ensure the backend is running on port `8000`
- Confirm the API origin is allowed by CORS
- Verify `FRONTEND_ORIGIN` matches the frontend address

### No results found
- Upload a valid `.md`, `.txt`, or `.pdf` file
- Keep files small enough under the configured upload limit
- Check that indexing completed successfully from the backend response

### LLM answer unavailable
- Validate your model credentials and access to the selected provider
- Ensure the selected model is supported and available
- Check the logs for generation errors or missing dependencies

---

## Future improvements

Potential next steps for the project:
- support more file formats such as DOCX and HTML
- add user authentication and per-user document storage
- improve citation quality and answer validation
- add vector database scaling and indexing performance tuning
- support multi-project onboarding and repo metadata extraction
- integrate GitHub API to analyze repositories and provide context-aware suggestions

---

## Summary

zerTrace is a practical RAG-based contribution assistant that helps users navigate project documentation using AI. It combines document ingestion, semantic search, hybrid retrieval, and LLM answer generation to create a user-friendly onboarding experience for first-time contributors.

The project is intentionally lightweight and easy to run locally, making it suitable for demos, experimentation, and extension into a larger open-source contributor support platform.

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

Then open the frontend in the browser and upload your documentation.
