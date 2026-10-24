from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from app.rag.pipeline import Pipeline

router = APIRouter()
_sessions = {}

class ChatReq(BaseModel):
    question: str
    session_id: Optional[str] = None
    top_k: Optional[int] = None
    mode: Optional[str] = "hybrid"
    threshold: Optional[float] = None

@router.post("")
def chat(req: ChatReq):
    sid = req.session_id or "default"
    history = _sessions.setdefault(sid, [])
    p = Pipeline()
    r = p.answer(req.question, history=history, top_k=req.top_k, mode=req.mode or "hybrid", threshold=req.threshold)
    history.append({"q": req.question, "a": r["answer"]})
    _sessions[sid] = history[-10:]
    return r
