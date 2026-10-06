from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class SIn(BaseModel):
    batch_id: int
    qty: int
    price: float
    seller: str | None = None
    prescription: str | None = None

@router.post("/")
def create(data: SIn, db: Session = Depends(get_session)):
    b = db.execute(text("SELECT qty FROM batches WHERE id=:i"), {"i": data.batch_id}).fetchone()
    if not b: raise HTTPException(404, "Партия не найдена")
    if b[0] < data.qty: raise HTTPException(400, "Недостаточно товара")
    db.execute(text("""
        INSERT INTO sales (batch_id, qty, price, seller, prescription)
        VALUES (:batch_id,:qty,:price,:seller,:prescription)
    """), data.dict())
    db.execute(text("UPDATE batches SET qty = qty - :q WHERE id=:i"),
               {"q": data.qty, "i": data.batch_id})
    db.commit()
    return {"status": "ok"}

@router.get("/day/{date}")
def by_day(date: str, db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text("""
        SELECT s.id, m.name, s.qty, s.price, s.sold_at
        FROM sales s JOIN batches b ON b.id=s.batch_id
        JOIN medicines m ON m.id=b.medicine_id
        WHERE s.sold_at::date = :d
        ORDER BY s.sold_at DESC
    """), {"d": date}).fetchall()]
