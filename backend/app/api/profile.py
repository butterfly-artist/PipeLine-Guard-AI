from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/profile")
def profile_data():
    raise HTTPException(status_code=501, detail="Profile endpoint is not implemented in Stage 1")
