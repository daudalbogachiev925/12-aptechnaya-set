from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class BIn(BaseModel):
    medicine_id: int
    pharmacy_id: int
    supplier_id: int
    qty: int
    price: float
    purchase_price: float | None = None
    expiry: date

@router.post("/")
def create(data: BIn, db: Session = Depends(get_session)):
    row = db.execute(text("""
        INSERT INTO batches (medicine_id, pharmacy_id, supplier_id, qty, price, purchase_price, expiry)
        VALUES (:medicine_id,:pharmacy_id,:supplier_id,:qty,:price,:purchase_price,:expiry)
        RETURNING id
    """), data.dict()).fetchone()
    db.commit()
    return {"id": row[0]}

@router.get("/pharmacy/{pharmacy_id}")
def by_pharmacy(pharmacy_id: int, db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text("""
        SELECT b.*, m.name AS medicine
        FROM batches b JOIN medicines m ON m.id=b.medicine_id
        WHERE b.pharmacy_id=:p
        ORDER BY b.expiry
    """), {"p": pharmacy_id}).fetchall()]
