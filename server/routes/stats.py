from fastapi import APIRouter, HTTPException
from services.stats_service import StatsService

router = APIRouter()

@router.get("/stats")
def get_stats():
    try:
        return StatsService.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
