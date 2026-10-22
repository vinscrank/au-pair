from app.models import CandidateProfile, FamilyProfile, User
from app.vocab import (
    AGE_BAND_LABELS,
    ARRANGEMENT_LABELS,
    CARE_WINDOW_LABELS,
    DAY_LABELS,
    DUTY_LABELS,
    GENDER_LABELS,
    HOUSEHOLD_LABELS,
    LEVEL_LABELS,
    MIND_LABELS,
    START_LABELS,
)


def join_names(items: list[str]) -> str:
    items = [item for item in items if item]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f" and {items[-1]}"


def labelled(mapping: dict[str, str], values: list[str] | None) -> str:
    return join_names([mapping.get(value, value) for value in (values or []) if value])


def euro(amount: int) -> str:
    return f"€{amount:,}"


def short_pay(basis: str, amount: int | None, amount_max: int | None, negotiable: bool) -> str:
    suffix = {"weekly": "/week", "hourly": "/hour", "monthly": "/month"}.get(basis, "")
    if amount and amount_max and amount_max > amount:
        text = f"{euro(amount)}–{euro(amount_max)}{suffix}"
    elif amount:
        text = f"{euro(amount)}{suffix}"
    elif negotiable:
        return "Pay negotiable"
    else:
        return ""
    if negotiable:
        return f"{text}, negotiable"
    return text


def long_pay(basis: str, amount: int | None, amount_max: int | None, negotiable: bool) -> str:
    unit = {"weekly": "a week", "hourly": "an hour", "monthly": "a month"}.get(basis, "")
    if amount and amount_max and amount_max > amount:
        money = f"{euro(amount)}–{euro(amount_max)}"
    elif amount:
        money = euro(amount)
    else:
        money = ""
    if basis == "weekly" and money:
        text = f"{money} a week pocket money"
    elif money and unit:
        text = f"{money} {unit}"
    elif negotiable:
        return "Negotiable"
    else:
        return ""
    if negotiable:
        return f"{text}, negotiable"
    return text


def format_languages(items: list | None) -> str:
    parts: list[str] = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        language = (item.get("language") or "").strip()
        level = LEVEL_LABELS.get(item.get("level") or "", "")
        if language:
            parts.append(f"{language} ({level})" if level else language)
    return ", ".join(parts)


def format_child(child: dict) -> str:
    years = child.get("age_years")
    months = child.get("age_months") or 0
    if years is None:
        return ""
    if years == 0:
        return f"{months} months" if months else "under 1"
    if months:
        year_word = "year" if years == 1 else "years"
        return f"{years} {year_word} {months} months"
    if years == 1:
        return "1 year"
    return f"{years} years"


def children_phrase(children: list | None, with_count: bool) -> str:
    parts = [format_child(child) for child in (children or []) if isinstance(child, dict)]
    parts = [part for part in parts if part]
    if not parts:
        return ""
    if not with_count:
        return join_names(parts)
    noun = "child" if len(parts) == 1 else "children"
    return f"{len(parts)} {noun}, {join_names(parts)}"


def short_areas(areas: list[str] | None) -> str:
    names = [area for area in (areas or []) if area]
    if not names:
        return ""
    if len(names) <= 2:
        return join_names(names)
    return f"{names[0]}, {names[1]} +{len(names) - 2}"


def experience_phrase(years: int | None) -> str:
    if years is None:
        return ""
    if years == 0:
        return "New to paid childcare"
    if years == 1:
        return "1 year of experience"
    return f"{years} years of experience"


def rows(*pairs: tuple[str, str]) -> list[dict[str, str]]:
    built: list[dict[str, str]] = []
    for label, value in pairs:
        text = (value or "").strip()
        if text:
            built.append({"label": label, "value": text})
    return built


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def section(title: str, body: list[dict[str, str]]) -> dict | None:
    if not body:
        return None
    return {"title": title, "rows": body}


def sections(*items: dict | None) -> list[dict]:
    return [item for item in items if item]


def duration_phrase(months: int | None) -> str:
    if not months:
        return ""
    if months == 1:
        return "1 month"
    return f"{months} months"


def hours_phrase(hours: int | None) -> str:
    if not hours:
        return ""
    return f"{hours} hours a week"


def candidate_card(user: User, profile: CandidateProfile) -> dict:
    headline_bits = []
    if profile.age:
        headline_bits.append(str(profile.age))
    if profile.nationality:
        headline_bits.append(profile.nationality.strip())
    practical = rows(
        ("Smoking", "Non-smoker" if profile.smoker is False else "Smoker" if profile.smoker is True else ""),
        ("Driving licence", yes_no(profile.has_driving_licence)),
        ("Own car", yes_no(profile.has_own_car)),
        ("Comfortable with pets", "Yes" if profile.comfortable_with_pets else ""),
        ("EU passport", "Yes" if profile.eu_passport else ""),
        ("Available at short notice", "Yes" if profile.available_short_notice else ""),
        ("First aid", "Yes" if profile.first_aid else ""),
        ("Garda vetting", "Self-reported, not checked by Mobijob" if profile.garda_vetting else ""),
        ("References", "Available" if profile.has_references else ""),
        ("Special needs experience", "Yes" if profile.special_needs_experience else ""),
        ("Qualification", profile.qualification or ""),
    )
    built = [
        section(
            "About",
            rows(
                ("Based in", profile.based_in or ""),
                ("Gender", GENDER_LABELS.get(profile.gender or "", "")),
                ("Languages", format_languages(profile.languages)),
            ),
        ),
        section(
            "Experience",
            rows(
                ("Experience", experience_phrase(profile.experience_years)),
                ("Ages minded", labelled(AGE_BAND_LABELS, profile.experience_age_bands)),
                ("In their own words", profile.experience_summary or ""),
            ),
        ),
        section(
            "The work",
            rows(
                ("Arrangement", ARRANGEMENT_LABELS.get(profile.arrangement or "", "")),
                ("Areas", join_names(profile.areas or [])),
                ("Where they can mind", labelled(MIND_LABELS, profile.minds_in)),
                ("Duties", labelled(DUTY_LABELS, profile.duties)),
                ("Days", labelled(DAY_LABELS, profile.days_available)),
                ("Hours", hours_phrase(profile.hours_per_week)),
                ("Typical week", profile.schedule_notes or ""),
                ("Can start", START_LABELS.get(profile.start_timing or "", "")),
                ("Can stay", duration_phrase(profile.duration_months)),
                ("Pay", long_pay(profile.pay_basis, profile.pay_min, profile.pay_max, profile.pay_negotiable)),
            ),
        ),
        section("Practical", practical),
    ]
    highlights = [
        ARRANGEMENT_LABELS.get(profile.arrangement or "", ""),
        short_areas(profile.areas),
        experience_phrase(profile.experience_years),
        short_pay(profile.pay_basis, profile.pay_min, profile.pay_max, profile.pay_negotiable),
        START_LABELS.get(profile.start_timing or "", ""),
    ]
    return {
        "user_id": str(user.id),
        "role": "candidate",
        "display_name": profile.display_name or "Candidate",
        "photo_url": profile.photo_url or "",
        "kicker": "Au pair or babysitter",
        "headline": " · ".join(headline_bits),
        "highlights": [item for item in highlights if item][:5],
        "bio": profile.bio or "",
        "sections": sections(*built),
    }


def family_card(user: User, profile: FamilyProfile) -> dict:
    room = ""
    if profile.arrangement in {"live_in", "either"} or profile.own_room:
        room = yes_no(profile.own_room)
    built = [
        section(
            "Children",
            rows(("Children", children_phrase(profile.children, with_count=True))),
        ),
        section(
            "When",
            rows(
                ("Schedule", profile.schedule_notes or ""),
                ("Days", labelled(DAY_LABELS, profile.days_needed)),
                ("Times", labelled(CARE_WINDOW_LABELS, profile.care_windows)),
                ("Hours", hours_phrase(profile.hours_per_week)),
                ("Can start", START_LABELS.get(profile.start_timing or "", "")),
                ("Hoping to host for", duration_phrase(profile.duration_months)),
            ),
        ),
        section(
            "The home",
            rows(
                ("Area", profile.area or ""),
                ("Household", HOUSEHOLD_LABELS.get(profile.household or "", "")),
                ("Languages at home", format_languages(profile.languages_at_home)),
                ("Arrangement", ARRANGEMENT_LABELS.get(profile.arrangement or "", "")),
                ("Duties", labelled(DUTY_LABELS, profile.duties)),
                ("Own room", room),
                ("Accommodation", profile.accommodation_notes or ""),
                ("Pets", (profile.pet_notes or "Yes") if profile.has_pets else ""),
            ),
        ),
        section(
            "Pay",
            rows(("Offered", long_pay(profile.pay_basis, profile.pay_amount, None, profile.pay_negotiable))),
        ),
    ]
    highlights = [
        children_phrase(profile.children, with_count=False),
        ARRANGEMENT_LABELS.get(profile.arrangement or "", ""),
        hours_phrase(profile.hours_per_week),
        short_pay(profile.pay_basis, profile.pay_amount, None, profile.pay_negotiable),
        START_LABELS.get(profile.start_timing or "", ""),
    ]
    return {
        "user_id": str(user.id),
        "role": "family",
        "display_name": profile.display_name or "Host family",
        "photo_url": profile.photo_url or "",
        "kicker": "Host family",
        "headline": profile.area or "Dublin",
        "highlights": [item for item in highlights if item][:5],
        "bio": profile.bio or "",
        "sections": sections(*built),
    }


def card_for(user: User, profile: CandidateProfile | FamilyProfile) -> dict:
    if isinstance(profile, CandidateProfile):
        return candidate_card(user, profile)
    return family_card(user, profile)
