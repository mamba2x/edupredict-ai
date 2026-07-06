from fastapi import APIRouter, HTTPException
from database import PredictionRepository

router = APIRouter()

@router.get("/records")
def get_records():
    try:
        total = PredictionRepository.get_record_count()
        records = PredictionRepository.get_recent_records()
        return {"records": records, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/records")
def clear_records():
    try:
        PredictionRepository.delete_all_records()
        return {"message": "All records deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
