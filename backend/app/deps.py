from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import COOKIE, parse_token


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(COOKIE)
    if not token:
        raise HTTPException(status_code=401, detail="Sign in to continue.")
    try:
        user_id = parse_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Sign in to continue.")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Sign in to continue.")
    return user
