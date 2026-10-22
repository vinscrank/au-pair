import re
import uuid

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.vocab import (
    AGE_BAND_VALUES,
    AREA_VALUES,
    ARRANGEMENT_VALUES,
    CARE_WINDOW_VALUES,
    DAY_VALUES,
    DUTY_VALUES,
    GENDER_VALUES,
    HOUSEHOLD_VALUES,
    LANGUAGE_VALUES,
    LEVEL_VALUES,
    MIND_VALUES,
    PAY_VALUES,
    START_VALUES,
)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RegisterIn(BaseModel):
    email: str
    password: str
    role: str

    @model_validator(mode="after")
    def check(self):
        self.email = self.email.strip().lower()
        if not EMAIL_RE.match(self.email):
            raise ValueError("Enter a valid email address.")
        if len(self.password) < 8:
            raise ValueError("Use at least 8 characters.")
        if self.role not in {"candidate", "family"}:
            raise ValueError("Choose candidate or family.")
        return self


class LoginIn(BaseModel):
    email: str
    password: str

    @model_validator(mode="after")
    def check(self):
        self.email = self.email.strip().lower()
        if not self.email or not self.password:
            raise ValueError("Enter your email and password.")
        return self


class SwipeIn(BaseModel):
    target_id: uuid.UUID
    direction: str

    @model_validator(mode="after")
    def check(self):
        if self.direction not in {"like", "pass"}:
            raise ValueError("Choose like or pass.")
        return self


class LanguageIn(BaseModel):
    language: str = ""
    level: str = ""


class ChildIn(BaseModel):
    age_years: int | None = None
    age_months: int | None = None


PAY_LIMIT = 9999


def euro(amount: int | None) -> int | None:
    if amount is None:
        return None
    if amount < 0 or amount > PAY_LIMIT:
        raise ValueError(f"Pay should be a whole number of euro up to {PAY_LIMIT}.")
    return amount


def bounded(value: str, limit: int, label: str) -> str:
    value = (value or "").strip()
    if len(value) > limit:
        raise ValueError(f"{label} is too long.")
    return value


def choice(value: str, allowed: set[str], label: str) -> str:
    value = (value or "").strip()
    if value and value not in allowed:
        raise ValueError(f"Choose a valid {label}.")
    return value


def choice_list(values: list[str], allowed: set[str], label: str, limit: int | None = None) -> list[str]:
    cleaned: list[str] = []
    for item in values:
        item = (item or "").strip()
        if not item:
            continue
        if item not in allowed:
            raise ValueError(f"Choose a valid {label}.")
        if item not in cleaned:
            cleaned.append(item)
    if limit is not None and len(cleaned) > limit:
        raise ValueError(f"Choose up to {limit} for {label}.")
    return cleaned


def tidy_languages(rows: list[LanguageIn]) -> list[LanguageIn]:
    kept: list[LanguageIn] = []
    seen: set[str] = set()
    for row in rows:
        language = row.language.strip()
        level = row.level.strip()
        if not language and not level:
            continue
        if not language or not level:
            raise ValueError("Choose a language and a level.")
        if language not in LANGUAGE_VALUES:
            raise ValueError("Choose a language from the list.")
        if level not in LEVEL_VALUES:
            raise ValueError("Choose a language level.")
        if language in seen:
            raise ValueError("List each language once.")
        seen.add(language)
        kept.append(LanguageIn(language=language, level=level))
    return kept


def photo_ok(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if ".." in value or not (value.startswith("/uploads/") or value.startswith("/seed/")):
        raise ValueError("Use a photo uploaded on Au pair.")
    return value


class CandidateIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    display_name: str = ""
    whatsapp: str = ""
    photo_url: str = ""
    age: int | None = Field(default=None, ge=18, le=75)
    gender: str = ""
    nationality: str = ""
    based_in: str = ""
    languages: list[LanguageIn] = []
    experience_years: int | None = Field(default=None, ge=0, le=60)
    experience_age_bands: list[str] = []
    experience_summary: str = ""
    qualification: str = ""
    first_aid: bool = False
    garda_vetting: bool = False
    has_references: bool = False
    smoker: bool | None = None
    comfortable_with_pets: bool = False
    has_driving_licence: bool = False
    has_own_car: bool = False
    eu_passport: bool = False
    special_needs_experience: bool = False
    duties: list[str] = []
    arrangement: str = ""
    areas: list[str] = []
    minds_in: list[str] = []
    days_available: list[str] = []
    hours_per_week: int | None = Field(default=None, ge=1, le=80)
    schedule_notes: str = ""
    available_short_notice: bool = False
    start_timing: str = ""
    duration_months: int | None = Field(default=None, ge=1, le=36)
    pay_basis: str = ""
    pay_min: int | None = None
    pay_max: int | None = None
    pay_negotiable: bool = False
    bio: str = ""

    @model_validator(mode="after")
    def tidy(self):
        self.display_name = bounded(self.display_name, 80, "Name")
        self.whatsapp = bounded(self.whatsapp, 32, "WhatsApp number")
        self.photo_url = photo_ok(self.photo_url)
        self.gender = choice(self.gender, GENDER_VALUES, "gender")
        self.nationality = bounded(self.nationality, 80, "Nationality")
        self.based_in = bounded(self.based_in, 120, "Where you are based")
        self.experience_summary = bounded(self.experience_summary, 800, "Experience")
        self.qualification = bounded(self.qualification, 160, "Qualification")
        self.schedule_notes = bounded(self.schedule_notes, 800, "Availability")
        self.bio = bounded(self.bio, 1500, "Bio")
        self.arrangement = choice(self.arrangement, ARRANGEMENT_VALUES, "arrangement")
        self.start_timing = choice(self.start_timing, START_VALUES, "start")
        self.pay_basis = choice(self.pay_basis, PAY_VALUES, "pay")
        self.pay_min = euro(self.pay_min)
        self.pay_max = euro(self.pay_max)
        self.experience_age_bands = choice_list(self.experience_age_bands, AGE_BAND_VALUES, "age group")
        self.duties = choice_list(self.duties, DUTY_VALUES, "duty")
        self.areas = choice_list(self.areas, AREA_VALUES, "area", limit=8)
        self.minds_in = choice_list(self.minds_in, MIND_VALUES, "place")
        self.days_available = choice_list(self.days_available, DAY_VALUES, "day")
        self.languages = tidy_languages(self.languages)
        if self.pay_min is not None and self.pay_max is not None and self.pay_max < self.pay_min:
            raise ValueError("The top of the pay range should be higher than the bottom.")
        return self


class FamilyIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    display_name: str = ""
    whatsapp: str = ""
    photo_url: str = ""
    area: str = ""
    children: list[ChildIn] = []
    schedule_notes: str = ""
    days_needed: list[str] = []
    hours_per_week: int | None = Field(default=None, ge=1, le=80)
    care_windows: list[str] = []
    start_timing: str = ""
    duration_months: int | None = Field(default=None, ge=1, le=36)
    arrangement: str = ""
    duties: list[str] = []
    languages_at_home: list[LanguageIn] = []
    household: str = ""
    has_pets: bool = False
    pet_notes: str = ""
    own_room: bool = False
    accommodation_notes: str = ""
    pay_basis: str = ""
    pay_amount: int | None = None
    pay_negotiable: bool = False
    bio: str = ""

    @model_validator(mode="after")
    def tidy(self):
        self.display_name = bounded(self.display_name, 80, "Name")
        self.whatsapp = bounded(self.whatsapp, 32, "WhatsApp number")
        self.photo_url = photo_ok(self.photo_url)
        self.area = choice(self.area, AREA_VALUES, "area")
        self.schedule_notes = bounded(self.schedule_notes, 800, "Schedule")
        self.pet_notes = bounded(self.pet_notes, 300, "Pet notes")
        self.accommodation_notes = bounded(self.accommodation_notes, 800, "Accommodation")
        self.bio = bounded(self.bio, 1500, "Bio")
        self.arrangement = choice(self.arrangement, ARRANGEMENT_VALUES, "arrangement")
        self.start_timing = choice(self.start_timing, START_VALUES, "start")
        self.pay_basis = choice(self.pay_basis, PAY_VALUES, "pay")
        self.pay_amount = euro(self.pay_amount)
        self.household = choice(self.household, HOUSEHOLD_VALUES, "household")
        self.duties = choice_list(self.duties, DUTY_VALUES, "duty")
        self.days_needed = choice_list(self.days_needed, DAY_VALUES, "day")
        self.care_windows = choice_list(self.care_windows, CARE_WINDOW_VALUES, "time of day")
        children: list[ChildIn] = []
        for child in self.children:
            if child.age_years is None and child.age_months is None:
                continue
            if child.age_years is None:
                raise ValueError("Add the child's age in years. Use 0 for under 1.")
            if not 0 <= child.age_years <= 17:
                raise ValueError("A child's age should be between 0 and 17.")
            if child.age_months is not None and not 0 <= child.age_months <= 11:
                raise ValueError("Months should be between 0 and 11.")
            children.append(ChildIn(age_years=child.age_years, age_months=child.age_months))
        if len(children) > 10:
            raise ValueError("Add up to 10 children.")
        self.children = children
        self.languages_at_home = tidy_languages(self.languages_at_home)
        return self
