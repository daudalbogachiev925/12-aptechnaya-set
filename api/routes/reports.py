from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

@router.get("/stock")
def stock(db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text(open('sql/stock.sql').read())).fetchall()]

@router.get("/expiry")
def expiry(days: int = 90, db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text("""
        SELECT m.name AS medicine, b.expiry, p.name AS pharmacy, b.qty,
               b.expiry - CURRENT_DATE AS days_left
        FROM batches b
        JOIN medicines m ON m.id=b.medicine_id
        JOIN pharmacies p ON p.id=b.pharmacy_id
        WHERE b.expiry < CURRENT_DATE + (:d || ' days')::interval AND b.qty>0
        ORDER BY b.expiry
    """), {"d": days}).fetchall()]

@router.get("/top")
def top(db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text(open('sql/top_medicines.sql').read())).fetchall()]

@router.get("/sales")
def sales(db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text(open('sql/sales.sql').read())).fetchall()]
