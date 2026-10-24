import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.rag.loader import clean_text
from app.rag.chunker import chunk_document

def test_chunks():
    text = "# H\n\nHello world. " * 20
    cs = chunk_document(clean_text(text), "f.md", "md", 100, 20, None)
    assert len(cs) > 0
    assert cs[0]["source"] == "f.md"
    assert cs[0]["section"] == "H"
