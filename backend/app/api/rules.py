from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/rules/generate")
def generate_rules():
    raise HTTPException(status_code=501, detail="Rules generation endpoint is not implemented in Stage 1")


@router.post("/rules/validate")
def validate_rules():
    raise HTTPException(status_code=501, detail="Rules validation endpoint is not implemented in Stage 1")
