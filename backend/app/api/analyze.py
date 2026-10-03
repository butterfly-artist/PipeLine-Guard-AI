from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/analyze")
def analyze_data():
    raise HTTPException(status_code=501, detail="Analyze endpoint is not implemented in Stage 1")
