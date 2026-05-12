import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import RequestHistory
from app.schemas import HistoryItem

router = APIRouter(prefix="/history", tags=["History"])
logger = logging.getLogger(__name__)

@router.get("", response_model=list[HistoryItem])
def get_history(db: Session = Depends(get_db)):
    logger.info("Fetching last 20 history items.")
    try:
        items = db.query(RequestHistory).order_by(RequestHistory.id.desc()).limit(20).all()
        return items
    except Exception as e:
        logger.error(f"DB error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/{record_id}", response_model=HistoryItem)
def get_history_item(record_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching history item ID: {record_id}")
    try:
        item = db.query(RequestHistory).filter(RequestHistory.id == record_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Record not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"DB error fetching item {record_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error")