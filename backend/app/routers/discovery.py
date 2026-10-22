from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.matching import discover_cards, list_matches, record_swipe
from app.models import User
from app.profiles import ensure_profile
from app.schemas import SwipeIn

router = APIRouter()


@router.get("/discover")
def discover(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ensure_profile(db, user)
    return {"cards": discover_cards(db, user)}


@router.post("/swipes")
def swipe(body: SwipeIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return record_swipe(db, user, body.target_id, body.direction)


@router.get("/matches")
def matches(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = ensure_profile(db, user)
    if not row.is_complete:
        raise HTTPException(status_code=403, detail="profile_incomplete")
    return {"matches": list_matches(db, user)}
