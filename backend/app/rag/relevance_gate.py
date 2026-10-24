from app.config import settings

def is_sufficient(results, threshold=None):
    if not results:
        return False, "No results retrieved."
    t = threshold if threshold is not None else settings.RELEVANCE_THRESHOLD
    # cosine distance: lower is better. Convert to similarity.
    sims = []
    for r in results:
        d = r.get("distance")
        if d is None:
            sims.append(1.0)
        else:
            sims.append(1.0 - d)
    top = max(sims) if sims else 0.0
    if top < t:
        return False, f"Top similarity {top:.2f} below threshold {t}."
    # require at least 2 supporting passages with reasonable sim
    good = [s for s in sims if s >= t*0.8]
    if len(good) < 1:
        return False, "Insufficient supporting evidence."
    return True, "Sufficient evidence."
