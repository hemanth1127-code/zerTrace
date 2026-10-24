def rrf_fuse(semantic, keyword, k=60):
    scores = {}
    for rank, item in enumerate(semantic):
        cid = item["chunk_id"]
        scores.setdefault(cid, {"item": item, "score": 0.0})
        scores[cid]["score"] += 1.0/(k + rank + 1)
    for rank, res in enumerate(keyword):
        cid = res["chunk"]["chunk_id"]
        it = {"chunk_id": cid, "text": res["chunk"]["text"], "metadata": {k:v for k,v in res["chunk"].items() if k!="text"}, "distance": None}
        scores.setdefault(cid, {"item": it, "score": 0.0})
        scores[cid]["score"] += 1.0/(k + rank + 1)
    fused = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return [f["item"] for f in fused], {f["item"]["chunk_id"]: f["score"] for f in fused}

class HybridRetriever:
    def __init__(self, vector_store, keyword):
        self.vs = vector_store
        self.kw = keyword

    def retrieve(self, q, q_emb, top_k=5, mode="hybrid"):
        sem = self.vs.query(q_emb, top_k*2) if mode in ("semantic", "hybrid") else []
        kw = self.kw.search(q, top_k*2) if mode in ("keyword", "hybrid") else []
        if mode == "semantic":
            return sem, {}
        if mode == "keyword":
            items = [{"chunk_id": r["chunk"]["chunk_id"], "text": r["chunk"]["text"], "metadata": {k:v for k,v in r["chunk"].items() if k!="text"}, "distance": None} for r in kw]
            return items, {}
        fused, sc = rrf_fuse(sem, kw)
        return fused[:top_k*2], sc
