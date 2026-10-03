import tempfile
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion import load_dataset
from app.profiling import profile_dataset
from app.quality import DQEngine, generate_default_rules
from app.core.contracts import DQRule, DQResult

router = APIRouter()


@router.post("/rules/generate")
async def generate_rules_endpoint(file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        file_path = tmp_dir_path / file.filename
        content = await file.read()
        file_path.write_bytes(content)

        try:
            df, meta = load_dataset(file_path)
            profile = profile_dataset(df, dataset_name=file.filename)
            rules = generate_default_rules(profile)
            return {"rules": rules}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.post("/rules/validate")
async def validate_rules_endpoint(
    file: UploadFile = File(...),
    rules: List[DQRule] = []
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        file_path = tmp_dir_path / file.filename
        content = await file.read()
        file_path.write_bytes(content)

        try:
            df, meta = load_dataset(file_path)
            engine = DQEngine({file.filename: df})
            results = engine.execute_rules(rules, primary_dataset_name=file.filename)
            return {
                "passed": sum(1 for r in results if r.status.value == "PASS"),
                "failed": sum(1 for r in results if r.status.value == "FAIL"),
                "results": results
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
