import os
from pathlib import Path

def load_document(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        import fitz
        doc = fitz.open(path)
        pages = []
        for i, page in enumerate(doc):
            pages.append({"page": i+1, "text": page.get_text()})
        doc.close()
        return pages
    if ext in (".md", ".txt"):
        with open(path, encoding="utf-8", errors="ignore") as f:
            return [{"page": None, "text": f.read()}]
    raise ValueError("Unsupported file type: " + ext)

def clean_text(text):
    import re
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()

def extract_sections(text):
    import re
    sections = []
    current = {"heading": "Document", "content": ""}
    for line in text.split("\n"):
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            if current["content"].strip():
                sections.append(current)
            current = {"heading": m.group(2).strip(), "content": ""}
        else:
            current["content"] += line + "\n"
    if current["content"].strip():
        sections.append(current)
    if not sections:
        sections = [{"heading": "Document", "content": text}]
    return sections
