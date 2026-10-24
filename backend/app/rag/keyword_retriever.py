from rank_bm25 import BM25Okapi
import re

class KeywordRetriever:
    def __init__(self):
        self.docs = []
        self.bm25 = None

    def build(self, chunks):
        self.docs = chunks
        tokenized = [re.findall(r"\w+", c["text"].lower()) for c in chunks]
        self.bm25 = BM25Okapi(tokenized) if chunks else None

    def search(self, q, k=5):
        if not self.bm25:
            return []
        tokens = re.findall(r"\w+", q.lower())
        scores = self.bm25.get_scores(tokens)
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [{"chunk": self.docs[i], "score": float(scores[i])} for i in ranked if scores[i] > 0]
