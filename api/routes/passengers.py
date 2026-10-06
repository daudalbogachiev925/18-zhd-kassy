from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class PIn(BaseModel):
    full_name: str
    passport: str
    birth: date | None = None
    phone: str | None = None

@router.post("/")
def create(data: PIn, db: Session = Depends(get_session)):
    row = db.execute(text("""
        INSERT INTO passengers (full_name, passport, birth, phone)
        VALUES (:full_name,:passport,:birth,:phone) RETURNING id
    """), data.dict()).fetchone()
    db.commit()
    return {"id": row[0]}

@router.get("/passport/{passport}")
def by_passport(passport: str, db: Session = Depends(get_session)):
    p = db.execute(text("SELECT * FROM passengers WHERE passport=:p"),
                   {"p": passport}).fetchone()
    return dict(p._mapping) if p else None
