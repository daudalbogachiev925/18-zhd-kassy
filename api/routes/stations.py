from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class SIn(BaseModel):
    name: str
    city: str | None = None
    code: str

@router.post("/")
def create(data: SIn, db: Session = Depends(get_session)):
    row = db.execute(text("""
        INSERT INTO stations (name, city, code) VALUES (:name,:city,:code) RETURNING id
    """), data.dict()).fetchone()
    db.commit()
    return {"id": row[0]}

@router.get("/")
def list_all(db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text("SELECT * FROM stations")).fetchall()]
