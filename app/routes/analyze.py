import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import RequestHistory
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.ml_service import analyze_text, MODEL_NAME

router = APIRouter(prefix="/analyze", tags=["Analyze"])
logger = logging.getLogger(__name__)

@router.post("", response_model=AnalyzeResponse, status_code=200)
def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    logger.info(f"Received text for analysis: '{req.text[:50]}...'")
    try:
        label, score = analyze_text(req.text)
        new_record = RequestHistory(
            input_text=req.text,
            result_text=f"{label} (score: {score:.4f})",
            model_name=MODEL_NAME
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        logger.info(f"Saved request ID {new_record.id} to DB.")
        return AnalyzeResponse(result=label, score=round(score, 4))
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to process request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis.")