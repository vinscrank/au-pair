from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.completion import missing_candidate, missing_family
from app.models import CandidateProfile, FamilyProfile, User
from app.present import card_for
from app.schemas import CandidateIn, FamilyIn


def ensure_profile(db: Session, user: User) -> CandidateProfile | FamilyProfile:
    model = CandidateProfile if user.role == "candidate" else FamilyProfile
    row = db.get(model, user.id)
    if row is None:
        row = model(user_id=user.id)
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


def missing_for(user: User, row: CandidateProfile | FamilyProfile) -> list[dict[str, str]]:
    if user.role == "candidate":
        return missing_candidate(row)
    return missing_family(row)


def refresh_completion(user: User, row: CandidateProfile | FamilyProfile) -> None:
    row.is_complete = len(missing_for(user, row)) == 0
    row.updated_at = datetime.now(timezone.utc)


def apply_profile(user: User, row: CandidateProfile | FamilyProfile, data: CandidateIn | FamilyIn) -> None:
    for key, value in data.model_dump().items():
        setattr(row, key, value)
    refresh_completion(user, row)


def dump_profile(user: User, row: CandidateProfile | FamilyProfile) -> dict:
    model = CandidateIn if user.role == "candidate" else FamilyIn
    return {key: getattr(row, key) for key in model.model_fields}


def profile_response(user: User, row: CandidateProfile | FamilyProfile) -> dict:
    return {
        "role": user.role,
        "complete": bool(row.is_complete),
        "missing": missing_for(user, row),
        "profile": dump_profile(user, row),
        "card": card_for(user, row),
    }


def me_dict(user: User, complete: bool) -> dict:
    return {
        "id": str(user.id),
        "email": user.email,
        "role": user.role,
        "profile_complete": complete,
    }
