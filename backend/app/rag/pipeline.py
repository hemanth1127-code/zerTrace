from app.config import settings
from app.rag.embeddings import embed_query
from app.rag.vector_store import query as vs_query
from app.rag.keyword_retriever import KeywordRetriever
from app.rag.hybrid_retriever import HybridRetriever
from app.rag.relevance_gate import is_sufficient
from app.rag.generator import generate_answer
from app.rag.citations import validate_citations

_kw = KeywordRetriever()
_hybrid = None

def init_keyword(chunks):
    global _kw, _hybrid
    _kw.build(chunks)
    from app.rag.vector_store import get_collection
    _hybrid = HybridRetriever(None, _kw)

def _vs_query(q_emb, k):
    return vs_query(q_emb, k)

class Pipeline:
    def __init__(self):
        self.hybrid = HybridRetriever(type("VS",(),{"query": lambda self,q,k: vs_query(q,k)})(), _kw)

    def answer(self, question, history=None, top_k=None, mode="hybrid", threshold=None):
        top_k = top_k or settings.TOP_K
        q_emb = embed_query(question)
        results, scores = self.hybrid.retrieve(question, q_emb, top_k=top_k, mode=mode)
        # attach distance handling
        ok, reason = is_sufficient(results, threshold)
        evidence = []
        for r in results:
            meta = r.get("metadata", {})
            evidence.append({
                "chunk_id": r["chunk_id"],
                "text": r["text"],
                "source": meta.get("source"),
                "section": meta.get("section"),
                "page": meta.get("page"),
                "file_type": meta.get("file_type"),
                "distance": r.get("distance"),
            })
        if not ok:
            return {"answer": "I couldn't find sufficient information to answer this question in the selected project's documentation. Try asking about the documented installation, development, testing, or contribution process.", "refused": True, "citations": [], "evidence": evidence, "reason": reason}
        # Use only top_k chunks for generation to reduce latency
        top_evidence = evidence[:top_k]
        allowed_ids = [e["chunk_id"] for e in top_evidence]
        context = "\n\n".join([f"[{e['chunk_id']}] {e['text']}" for e in top_evidence])
        try:
            raw = generate_answer(question, context, allowed_ids)
        except Exception as e:
            return {"answer": f"Generation unavailable: {e}", "refused": False, "citations": [], "evidence": evidence, "error": str(e)}
        valid, invalid = validate_citations(raw, allowed_ids)
        cites = []
        for cid in valid:
            rec = next((e for e in evidence if e["chunk_id"]==cid), None)
            if rec:
                cites.append({"chunk_id": cid, "source": rec["source"], "section": rec["section"], "page": rec["page"]})
        # dedupe
        seen=set(); uniq=[]
        for c in cites:
            if c["chunk_id"] not in seen:
                seen.add(c["chunk_id"]); uniq.append(c)
        return {"answer": raw, "refused": False, "citations": uniq, "evidence": evidence, "reason": None}
