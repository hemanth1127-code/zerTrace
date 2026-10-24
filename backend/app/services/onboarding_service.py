from app.rag.pipeline import Pipeline
from app.rag.embeddings import embed_query
from app.rag.vector_store import query as vs_query

def generate_roadmap():
    p = Pipeline()
    q = "How do I get started contributing to this project? setup installation development workflow tests pull request"
    res = p.answer(q, top_k=8)
    steps = []
    for i, e in enumerate(res["evidence"][:6], 1):
        steps.append({
            "step": i,
            "title": e["section"] or "Step",
            "description": e["text"][:400],
            "source": e["source"],
            "section": e["section"],
            "page": e["page"],
            "chunk_id": e["chunk_id"],
        })
    if not steps:
        steps = [{"step":1,"title":"No documentation found","description":"Index project docs first.","source":None,"section":None,"page":None,"chunk_id":None}]
    return {"steps": steps, "raw": res["answer"]}
