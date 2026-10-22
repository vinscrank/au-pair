import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.config import BACKEND_ROOT
from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.profiles import apply_profile, ensure_profile, profile_response, refresh_completion
from app.schemas import CandidateIn, FamilyIn

router = APIRouter()
UPLOAD_DIR = BACKEND_ROOT / "uploads"


def sniff(data: bytes) -> str | None:
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return None


@router.get("/profile")
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return profile_response(user, ensure_profile(db, user))


@router.put("/profile")
def update_profile(body: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    model = CandidateIn if user.role == "candidate" else FamilyIn
    try:
        data = model.model_validate(body)
    except ValidationError as exc:
        message = "Check the form and try again."
        errors = exc.errors()
        if errors:
            message = errors[0].get("msg", message)
            if message.startswith("Value error, "):
                message = message[len("Value error, ") :]
        raise HTTPException(status_code=422, detail=message)
    row = ensure_profile(db, user)
    apply_profile(user, row, data)
    db.commit()
    db.refresh(row)
    return profile_response(user, row)


@router.post("/profile/photo")
async def upload_photo(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await file.read()
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(status_code=422, detail="That photo is larger than 5MB.")
    extension = sniff(data)
    if not extension:
        raise HTTPException(status_code=422, detail="Use a JPG, PNG, or WebP photo.")
    UPLOAD_DIR.mkdir(exist_ok=True)
    name = f"{uuid.uuid4().hex}{extension}"
    Path(UPLOAD_DIR / name).write_bytes(data)
    row = ensure_profile(db, user)
    row.photo_url = f"/uploads/{name}"
    refresh_completion(user, row)
    db.commit()
    return {"photo_url": row.photo_url}
