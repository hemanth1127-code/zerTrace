from sentence_transformers import SentenceTransformer
from app.config import settings

_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model

def embed_texts(texts):
    m = get_model()
    return m.encode(texts, convert_to_numpy=True).tolist()

def embed_query(q):
    return embed_texts([q])[0]
