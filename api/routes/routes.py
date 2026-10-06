from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class RIn(BaseModel):
    train_id: int
    from_station_id: int
    to_station_id: int
    depart: datetime
    arrive: datetime
    base_price: float

@router.post("/")
def create(data: RIn, db: Session = Depends(get_session)):
    row = db.execute(text("""
        INSERT INTO routes (train_id, from_station_id, to_station_id, depart, arrive, base_price)
        VALUES (:train_id,:from_station_id,:to_station_id,:depart,:arrive,:base_price)
        RETURNING id
    """), data.dict()).fetchone()
    db.commit()
    return {"id": row[0]}

@router.get("/search")
def search(from_code: str, to_code: str, date: str,
           db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text("""
        SELECT r.id, t.number AS train_number, t.name AS train_name,
               s1.name AS from_st, s2.name AS to_st,
               r.depart, r.arrive, r.base_price
        FROM routes r
        JOIN trains t ON t.id = r.train_id
        JOIN stations s1 ON s1.id = r.from_station_id
        JOIN stations s2 ON s2.id = r.to_station_id
        WHERE s1.code = :f AND s2.code = :t AND r.depart::date = :d
        ORDER BY r.depart
    """), {"f": from_code, "t": to_code, "d": date}).fetchall()]
