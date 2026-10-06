from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

@router.get("/occupancy/{route_id}")
def occupancy(route_id: int, db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text(open('sql/seat_occupancy.sql').read()),
                                                 {"route_id": route_id}).fetchall()]

@router.get("/revenue")
def revenue(db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text(open('sql/revenue.sql').read())).fetchall()]

@router.get("/loading")
def loading(db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text(open('sql/loading.sql').read())).fetchall()]

@router.get("/refunds")
def refunds(db: Session = Depends(get_session)):
    return [dict(r._mapping) for r in db.execute(text(open('sql/refunds.sql').read())).fetchall()]
