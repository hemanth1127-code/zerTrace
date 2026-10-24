import json, os
from app.rag.pipeline import Pipeline

def run_evaluation():
    path = os.path.join(os.path.dirname(__file__), "questions.json")
    with open(path) as f:
        cases = json.load(f)
    p = Pipeline()
    results = []
    for c in cases:
        r = p.answer(c["question"])
        refused = r["refused"]
        expected_refuse = c.get("expected_refuse", False)
        ok = (refused == expected_refuse)
        results.append({"question": c["question"], "expected_refuse": expected_refuse, "refused": refused, "pass": ok, "category": c.get("category")})
    total = len(results)
    passed = sum(1 for r in results if r["pass"])
    return {"total": total, "passed": passed, "accuracy": passed/total if total else 0, "results": results}
