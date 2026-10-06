from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class TIn(BaseModel):
    car_id: int
    route_id: int
    passenger_id: int
    seat: int

@router.post("/")
def buy(data: TIn, db: Session = Depends(get_session)):
    car = db.execute(text("SELECT price, seats FROM cars WHERE id=:i"),
                     {"i": data.car_id}).fetchone()
    if not car: raise HTTPException(404, "Вагон не найден")
    if data.seat < 1 or data.seat > car[1]:
        raise HTTPException(400, "Место вне диапазона")
    already = db.execute(text("""
        SELECT 1 FROM tickets WHERE route_id=:r AND car_id=:c AND seat=:s AND status='booked'
    """), {"r": data.route_id, "c": data.car_id, "s": data.seat}).fetchone()
    if already: raise HTTPException(400, "Место занято")
    row = db.execute(text("""
        INSERT INTO tickets (car_id, route_id, passenger_id, seat, price)
        VALUES (:car_id,:route_id,:passenger_id,:seat,:price) RETURNING id
    """), {**data.dict(), "price": car[0]}).fetchone()
    db.commit()
    return {"ticket_id": row[0], "price": float(car[0])}

@router.post("/{ticket_id}/refund")
def refund(ticket_id: int, db: Session = Depends(get_session)):
    t = db.execute(text("SELECT status FROM tickets WHERE id=:i"), {"i": ticket_id}).fetchone()
    if not t: raise HTTPException(404)
    if t[0] != 'booked': raise HTTPException(400, "Возврат невозможен")
    db.execute(text("""
        UPDATE tickets SET status='refunded', refunded_at=NOW() WHERE id=:i
    """), {"i": ticket_id})
    db.commit()
    return {"status": "refunded", "refund_pct": 70}

@router.get("/passenger/{passenger_id}")
def by_passenger(passenger_id: int, db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text("""
        SELECT tk.id, t.number AS train, s1.name AS from_st, s2.name AS to_st,
               r.depart, c.number AS car, tk.seat, tk.price, tk.status
        FROM tickets tk
        JOIN routes r ON r.id = tk.route_id
        JOIN trains t ON t.id = r.train_id
        JOIN stations s1 ON s1.id = r.from_station_id
        JOIN stations s2 ON s2.id = r.to_station_id
        JOIN cars c ON c.id = tk.car_id
        WHERE tk.passenger_id = :p ORDER BY r.depart DESC
    """), {"p": passenger_id}).fetchall()]
