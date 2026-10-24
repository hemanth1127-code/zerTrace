from fastapi import APIRouter
from app.evaluation.evaluator import run_evaluation
router = APIRouter()
@router.post("/run")
def run():
    return run_evaluation()
