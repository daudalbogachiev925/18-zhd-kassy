from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class CIn(BaseModel):
    route_id: int
    number: str
    car_type: str
    seats: int
    price: float

@router.post("/")
def create(data: CIn, db: Session = Depends(get_session)):
    row = db.execute(text("""
        INSERT INTO cars (route_id, number, car_type, seats, price)
        VALUES (:route_id,:number,:car_type,:seats,:price) RETURNING id
    """), data.dict()).fetchone()
    db.commit()
    return {"id": row[0]}

@router.get("/route/{route_id}")
def by_route(route_id: int, db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text("""
        SELECT * FROM cars WHERE route_id=:r ORDER BY number
    """), {"r": route_id}).fetchall()]
