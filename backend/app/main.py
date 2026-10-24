from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import documents, chat, onboarding, evaluation

origins = list(dict.fromkeys([
    settings.FRONTEND_ORIGIN,
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]))

app = FastAPI(title="ContribGuide AI")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    from app.rag.vector_store import count
    return {"status": "ok", "chunks": count(), "model": settings.GEMMA_MODEL}

app.include_router(documents.router, prefix="/api/documents")
app.include_router(chat.router, prefix="/api/chat")
app.include_router(onboarding.router, prefix="/api/onboarding")
app.include_router(evaluation.router, prefix="/api/evaluation")
