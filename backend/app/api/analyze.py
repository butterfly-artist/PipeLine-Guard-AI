import tempfile
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import analysis_service

router = APIRouter()


@router.post("/analyze")
async def analyze_endpoint(
    files: List[UploadFile] = File(...),
    log_file: Optional[UploadFile] = File(None)
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        tmp_paths: List[Path] = []
        tmp_log_path: Optional[Path] = None

        try:
            for f in files:
                content = await f.read()
                file_path = tmp_dir_path / f.filename
                file_path.write_bytes(content)
                tmp_paths.append(file_path)

            if log_file:
                log_content = await log_file.read()
                tmp_log_path = tmp_dir_path / (log_file.filename or "pipeline.log")
                tmp_log_path.write_bytes(log_content)

            response = analysis_service.analyze(
                dataset_paths=tmp_paths,
                log_path=tmp_log_path
            )
            return response

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo")
def demo_endpoint():
    """Run end-to-end analysis on CartFlow example dataset."""
    base_dir = Path(__file__).parent.parent.parent.parent
    cartflow_dir = base_dir / "examples" / "cartflow"

    orders_path = cartflow_dir / "orders.csv"
    payments_path = cartflow_dir / "payments.csv"
    items_path = cartflow_dir / "order_items.parquet"
    sellers_path = cartflow_dir / "sellers.json"
    log_path = cartflow_dir / "pipeline.log"

    dataset_paths = [p for p in [orders_path, payments_path, items_path, sellers_path] if p.exists()]
    if not dataset_paths:
        raise HTTPException(status_code=404, detail="CartFlow demo dataset files not found.")

    return analysis_service.analyze(
        dataset_paths=dataset_paths,
        log_path=log_path if log_path.exists() else None
    )
