from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class PhIn(BaseModel):
    name: str
    address: str | None = None
    phone: str | None = None
    city: str | None = None

@router.post("/")
def create(data: PhIn, db: Session = Depends(get_session)):
    row = db.execute(text("""
        INSERT INTO pharmacies (name, address, phone, city)
        VALUES (:name,:address,:phone,:city) RETURNING id
    """), data.dict()).fetchone()
    db.commit()
    return {"id": row[0]}

@router.get("/")
def list_all(city: str | None = None, db: Session = Depends(get_session)):
    sql = "SELECT * FROM pharmacies"
    params = {}
    if city:
        sql += " WHERE city = :c"
        params['c'] = city
    return [dict(r._mapping) for r in db.execute(text(sql), params).fetchall()]
