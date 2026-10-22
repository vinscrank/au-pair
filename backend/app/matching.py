import uuid

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.contact_gate import contact_view
from app.models import CandidateProfile, FamilyProfile, Match, Swipe, User
from app.present import candidate_card, family_card
from app.profiles import ensure_profile


def ordered_ids(left: uuid.UUID, right: uuid.UUID) -> tuple[uuid.UUID, uuid.UUID]:
    if str(left) < str(right):
        return left, right
    return right, left


def discover_cards(db: Session, user: User) -> list[dict]:
    row = ensure_profile(db, user)
    if not row.is_complete:
        raise HTTPException(status_code=403, detail="profile_incomplete")
    swiped = select(Swipe.target_id).where(Swipe.swiper_id == user.id)
    cards: list[dict] = []
    if user.role == "candidate":
        profiles = db.scalars(
            select(FamilyProfile)
            .where(FamilyProfile.is_complete.is_(True))
            .where(FamilyProfile.user_id.notin_(swiped))
            .order_by(FamilyProfile.updated_at.desc())
        ).all()
        for profile in profiles:
            other = db.get(User, profile.user_id)
            if other and other.role == "family":
                cards.append(family_card(other, profile))
        return cards
    profiles = db.scalars(
        select(CandidateProfile)
        .where(CandidateProfile.is_complete.is_(True))
        .where(CandidateProfile.user_id.notin_(swiped))
        .order_by(CandidateProfile.updated_at.desc())
    ).all()
    for profile in profiles:
        other = db.get(User, profile.user_id)
        if other and other.role == "candidate":
            cards.append(candidate_card(other, profile))
    return cards


def match_payload(viewer: User, other: User, other_profile: CandidateProfile | FamilyProfile, row: Match) -> dict:
    created = row.created_at.isoformat() if row.created_at else None
    card = candidate_card(other, other_profile) if isinstance(other_profile, CandidateProfile) else family_card(other, other_profile)
    return {
        "id": str(row.id),
        "created_at": created,
        "card": card,
        "contact": contact_view(
            is_mutual_match=True,
            viewer_id=viewer.id,
            whatsapp=other_profile.whatsapp,
        ),
    }


def list_matches(db: Session, user: User) -> list[dict]:
    rows = db.scalars(
        select(Match)
        .where(or_(Match.user_low_id == user.id, Match.user_high_id == user.id))
        .order_by(Match.created_at.desc())
    ).all()
    payload: list[dict] = []
    for row in rows:
        other_id = row.user_high_id if row.user_low_id == user.id else row.user_low_id
        other = db.get(User, other_id)
        if not other:
            continue
        model = CandidateProfile if other.role == "candidate" else FamilyProfile
        profile = db.get(model, other.id)
        if not profile:
            continue
        payload.append(match_payload(user, other, profile, row))
    return payload


def record_swipe(db: Session, user: User, target_id: uuid.UUID, direction: str) -> dict:
    row = ensure_profile(db, user)
    if not row.is_complete:
        raise HTTPException(status_code=403, detail="profile_incomplete")
    if target_id == user.id:
        raise HTTPException(status_code=422, detail="You can't choose your own profile.")
    target = db.get(User, target_id)
    if not target or target.role == user.role:
        raise HTTPException(status_code=404, detail="That profile is not available.")
    target_model = CandidateProfile if target.role == "candidate" else FamilyProfile
    target_profile = db.get(target_model, target.id)
    if not target_profile or not target_profile.is_complete:
        raise HTTPException(status_code=404, detail="That profile is not available.")
    existing = db.scalar(select(Swipe).where(Swipe.swiper_id == user.id, Swipe.target_id == target_id))
    if existing:
        raise HTTPException(status_code=409, detail="You have already responded to this profile.")
    db.add(Swipe(swiper_id=user.id, target_id=target_id, direction=direction))
    match_row = None
    if direction == "like":
        reciprocal = db.scalar(
            select(Swipe).where(
                Swipe.swiper_id == target_id,
                Swipe.target_id == user.id,
                Swipe.direction == "like",
            )
        )
        if reciprocal:
            low, high = ordered_ids(user.id, target_id)
            match_row = db.scalar(select(Match).where(Match.user_low_id == low, Match.user_high_id == high))
            if match_row is None:
                match_row = Match(user_low_id=low, user_high_id=high)
                db.add(match_row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="You have already responded to this profile.")
    if match_row is None:
        return {"direction": direction, "matched": False, "match": None}
    db.refresh(match_row)
    return {
        "direction": direction,
        "matched": True,
        "match": match_payload(user, target, target_profile, match_row),
    }
