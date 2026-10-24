import os, chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings

_client = None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is None:
        os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        _client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
        _collection = _client.get_or_create_collection("contribguide", metadata={"hnsw:space": "cosine"})
    return _collection

def add_chunks(chunks, embeddings):
    col = get_collection()
    col.add(
        ids=[c["chunk_id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=[{k: (v if v is not None else "") for k, v in c.items() if k not in ("text",)} for c in chunks],
    )

def query(q_emb, k=5):
    col = get_collection()
    res = col.query(query_embeddings=[q_emb], n_results=k)
    out = []
    for i, cid in enumerate(res["ids"][0]):
        out.append({
            "chunk_id": cid,
            "text": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
            "distance": res["distances"][0][i],
        })
    return out

def count():
    return get_collection().count()

def delete_by_source(source):
    col = get_collection()
    try:
        col.delete(where={"source": source})
    except Exception:
        pass

def clear():
    global _collection
    _collection = None
    try:
        import shutil
        if os.path.exists(settings.CHROMA_PERSIST_DIRECTORY):
            shutil.rmtree(settings.CHROMA_PERSIST_DIRECTORY)
    except Exception:
        pass
