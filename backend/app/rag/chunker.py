from .loader import extract_sections, clean_text

def chunk_document(text, source, file_type, chunk_size=800, overlap=150, page=None):
    chunks = []
    idx = 0
    for sec in extract_sections(text):
        content = clean_text(sec["content"])
        if not content:
            continue
        start = 0
        while start < len(content):
            end = min(start + chunk_size, len(content))
            piece = content[start:end]
            chunks.append({
                "chunk_id": f"{source}_{idx:04d}".replace(" ", "_").replace("/", "_"),
                "text": piece,
                "source": source,
                "section": sec["heading"],
                "page": page,
                "file_type": file_type,
            })
            idx += 1
            if end >= len(content):
                break
            start = end - overlap
            if start < 0:
                start = 0
    return chunks
