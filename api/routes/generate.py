from fastapi import APIRouter, Depends
from api.auth.deps import get_current_user
from api.schemas import GenerateRequest, GenerateResponse
from core.ai.ai_engine import generate_text

router = APIRouter()

@router.post("/", response_model=GenerateResponse)
def generate(
    payload: GenerateRequest,
    user=Depends(get_current_user)
):
    result = generate_text(payload.prompt)
    return GenerateResponse(result=result)
