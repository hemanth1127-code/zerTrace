def validate_citations(answer_text, allowed_ids):
    import re
    found = re.findall(r"\[([^\]]+)\]", answer_text)
    valid = [c for c in found if c in allowed_ids]
    invalid = [c for c in found if c not in allowed_ids]
    return valid, invalid
