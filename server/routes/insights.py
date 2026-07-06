from fastapi import APIRouter, HTTPException
import json
import os
from config import MODEL_DIR

router = APIRouter()

@router.get("/insights")
def get_insights():
    try:
        with open(os.path.join(MODEL_DIR, "insights.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Insights not found. Run train.py first.")
