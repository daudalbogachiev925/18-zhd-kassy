from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class TIn(BaseModel):
    number: str
    name: str | None = None
    train_type: str | None = None

@router.post("/")
def create(data: TIn, db: Session = Depends(get_session)):
    row = db.execute(text("""
        INSERT INTO trains (number, name, train_type)
        VALUES (:number,:name,:train_type) RETURNING id
    """), data.dict()).fetchone()
    db.commit()
    return {"id": row[0]}

@router.get("/")
def list_all(db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text("SELECT * FROM trains")).fetchall()]
