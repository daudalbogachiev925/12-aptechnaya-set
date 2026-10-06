from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class MIn(BaseModel):
    name: str
    form: str | None = None
    manufacturer: str | None = None
    rx: bool = False
    category: str | None = None

@router.post("/")
def create(data: MIn, db: Session = Depends(get_session)):
    row = db.execute(text("""
        INSERT INTO medicines (name, form, manufacturer, rx, category)
        VALUES (:name,:form,:manufacturer,:rx,:category) RETURNING id
    """), data.dict()).fetchone()
    db.commit()
    return {"id": row[0]}

@router.get("/")
def list_all(q: str | None = None, db: Session = Depends(get_session)):
    sql = "SELECT * FROM medicines"
    params = {}
    if q:
        sql += " WHERE name ILIKE :q"
        params['q'] = f"%{q}%"
    return [dict(r._mapping) for r in db.execute(text(sql), params).fetchall()]

@router.get("/{med_id}")
def get(med_id: int, db: Session = Depends(get_session)):
    m = db.execute(text("SELECT * FROM medicines WHERE id=:i"), {"i": med_id}).fetchone()
    if not m: raise HTTPException(404)
    return dict(m._mapping)
