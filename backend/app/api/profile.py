import tempfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion import load_dataset
from app.profiling import profile_dataset

router = APIRouter()


@router.post("/profile")
async def profile_data_endpoint(file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        file_path = tmp_dir_path / file.filename
        content = await file.read()
        file_path.write_bytes(content)

        try:
            df, meta = load_dataset(file_path)
            profile = profile_dataset(df, dataset_name=file.filename)
            return profile
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
