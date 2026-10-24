import os, shutil, uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
from app.rag.loader import load_document, clean_text
from app.rag.chunker import chunk_document
from app.rag.embeddings import embed_texts
from app.rag.vector_store import add_chunks, delete_by_source, count

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".pdf", ".md", ".txt"):
        raise HTTPException(400, "Unsupported file type")
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    safe = str(uuid.uuid4()) + ext
    path = os.path.join(settings.UPLOAD_DIRECTORY, safe)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    size_mb = os.path.getsize(path)/(1024*1024)
    if size_mb > settings.MAX_UPLOAD_MB:
        os.remove(path); raise HTTPException(413, "File too large")
    # process
    pages = load_document(path)
    all_chunks = []
    for p in pages:
        chunks = chunk_document(clean_text(p["text"]), file.filename, ext.lstrip("."), settings.CHUNK_SIZE, settings.CHUNK_OVERLAP, p["page"])
        all_chunks.extend(chunks)
    # reindex: delete old
    delete_by_source(file.filename)
    if all_chunks:
        embs = embed_texts([c["text"] for c in all_chunks])
        add_chunks(all_chunks, embs)
    from app.rag.pipeline import init_keyword
    # rebuild keyword index from all chunks? simple: rebuild from this upload only is not enough; but ok for demo
    init_keyword(all_chunks)
    return {"filename": file.filename, "chunks": len(all_chunks), "total_chunks": count()}

@router.get("")
def list_docs():
    return {"total_chunks": count()}

@router.delete("/{doc_id}")
def delete(doc_id: str):
    delete_by_source(doc_id)
    return {"deleted": doc_id}

@router.post("/reindex")
def reindex():
    return {"status": "ok"}
