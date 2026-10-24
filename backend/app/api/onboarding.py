from fastapi import APIRouter
from app.services.onboarding_service import generate_roadmap
router = APIRouter()
@router.post("")
def onboarding():
    return generate_roadmap()
