import re

from app.models import CandidateProfile, FamilyProfile
from app.vocab import ARRANGEMENT_LABELS, START_LABELS


def phone_ok(value: str) -> bool:
    return len(re.sub(r"\D", "", value or "")) >= 7


def text_ok(value: str | None, minimum: int) -> bool:
    return len((value or "").strip()) >= minimum


def miss(items: list[dict[str, str]], key: str, label: str, ok: bool) -> None:
    if not ok:
        items.append({"key": key, "label": label})


def missing_candidate(profile: CandidateProfile) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    miss(items, "display_name", "Name", text_ok(profile.display_name, 2))
    miss(items, "whatsapp", "WhatsApp number", phone_ok(profile.whatsapp))
    miss(items, "photo_url", "Photo", bool((profile.photo_url or "").strip()))
    miss(items, "age", "Age", profile.age is not None and 18 <= profile.age <= 75)
    miss(items, "nationality", "Nationality", text_ok(profile.nationality, 2))
    miss(items, "based_in", "Where you are based", text_ok(profile.based_in, 2))
    miss(items, "languages", "Languages", bool(profile.languages))
    miss(items, "experience_years", "Years of experience", profile.experience_years is not None and profile.experience_years >= 0)
    miss(items, "experience_age_bands", "Ages you have minded", bool(profile.experience_age_bands))
    miss(items, "arrangement", "Live-in or live-out", profile.arrangement in ARRANGEMENT_LABELS)
    miss(items, "areas", "Dublin areas", bool(profile.areas))
    miss(items, "minds_in", "Where you can mind", bool(profile.minds_in))
    miss(items, "duties", "Duties", bool(profile.duties))
    miss(items, "smoker", "Smoking", profile.smoker is True or profile.smoker is False)
    miss(items, "schedule_notes", "When you are available", text_ok(profile.schedule_notes, 10))
    miss(items, "start_timing", "When you can start", profile.start_timing in START_LABELS)
    pay_amount_ok = profile.pay_negotiable or (profile.pay_min or 0) > 0
    if not profile.pay_basis:
        miss(items, "pay_basis", "Pay", False)
    elif not pay_amount_ok:
        miss(items, "pay_min", "Expected pay", False)
    miss(items, "bio", "Short bio", text_ok(profile.bio, 20))
    return items


def missing_family(profile: FamilyProfile) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    ages = [child for child in (profile.children or []) if child.get("age_years") is not None]
    miss(items, "display_name", "Name", text_ok(profile.display_name, 2))
    miss(items, "whatsapp", "WhatsApp number", phone_ok(profile.whatsapp))
    miss(items, "photo_url", "Photo", bool((profile.photo_url or "").strip()))
    miss(items, "area", "Where you need care", bool((profile.area or "").strip()))
    miss(items, "children", "Children's ages", len(ages) >= 1)
    miss(items, "schedule_notes", "When you need care", text_ok(profile.schedule_notes, 10))
    miss(items, "hours_per_week", "Hours a week", profile.hours_per_week is not None and profile.hours_per_week > 0)
    miss(items, "start_timing", "When you want to start", profile.start_timing in START_LABELS)
    miss(items, "arrangement", "Live-in or live-out", profile.arrangement in ARRANGEMENT_LABELS)
    miss(items, "duties", "Duties", bool(profile.duties))
    miss(items, "languages_at_home", "Languages at home", bool(profile.languages_at_home))
    if profile.arrangement in {"live_in", "either"}:
        miss(items, "own_room", "Own room", bool(profile.own_room))
        miss(items, "accommodation_notes", "Accommodation", text_ok(profile.accommodation_notes, 10))
    pay_amount_ok = profile.pay_negotiable or (profile.pay_amount or 0) > 0
    if not profile.pay_basis:
        miss(items, "pay_basis", "Pay", False)
    elif not pay_amount_ok:
        miss(items, "pay_amount", "Pay offered", False)
    miss(items, "bio", "Short bio", text_ok(profile.bio, 20))
    return items
