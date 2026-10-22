from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import CandidateProfile, FamilyProfile, User
from app.profiles import ensure_profile, me_dict
from app.schemas import LoginIn, RegisterIn
from app.security import clear_session_cookie, hash_password, set_session_cookie, verify_password

router = APIRouter()


@router.post("/auth/register")
def register(body: RegisterIn, response: Response, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == body.email))
    if existing:
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    user = User(email=body.email, password_hash=hash_password(body.password), role=body.role)
    db.add(user)
    db.flush()
    profile_model = CandidateProfile if body.role == "candidate" else FamilyProfile
    db.add(profile_model(user_id=user.id))
    db.commit()
    set_session_cookie(response, user.id)
    return me_dict(user, False)


@router.post("/auth/login")
def login(body: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email))
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is not right.")
    row = ensure_profile(db, user)
    set_session_cookie(response, user.id)
    return me_dict(user, bool(row.is_complete))


@router.post("/auth/logout", status_code=204)
def logout(response: Response) -> None:
    clear_session_cookie(response)


@router.get("/auth/me")
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = ensure_profile(db, user)
    return me_dict(user, bool(row.is_complete))
