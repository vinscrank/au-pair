import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def new_id() -> uuid.UUID:
    return uuid.uuid4()


class User(Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("role in ('candidate', 'family')", name="ck_users_role"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_id)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    display_name: Mapped[str] = mapped_column(String(80), default="", server_default="")
    whatsapp: Mapped[str] = mapped_column(String(32), default="", server_default="")
    photo_url: Mapped[str] = mapped_column(String(400), default="", server_default="")
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str] = mapped_column(String(32), default="", server_default="")
    nationality: Mapped[str] = mapped_column(String(80), default="", server_default="")
    based_in: Mapped[str] = mapped_column(String(120), default="", server_default="")
    languages: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    experience_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    experience_age_bands: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    experience_summary: Mapped[str] = mapped_column(Text, default="", server_default="")
    qualification: Mapped[str] = mapped_column(String(160), default="", server_default="")
    first_aid: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    garda_vetting: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    has_references: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    smoker: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    comfortable_with_pets: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    has_driving_licence: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    has_own_car: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    eu_passport: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    special_needs_experience: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    duties: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    arrangement: Mapped[str] = mapped_column(String(32), default="", server_default="")
    areas: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    minds_in: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    days_available: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    hours_per_week: Mapped[int | None] = mapped_column(Integer, nullable=True)
    schedule_notes: Mapped[str] = mapped_column(Text, default="", server_default="")
    available_short_notice: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    start_timing: Mapped[str] = mapped_column(String(32), default="", server_default="")
    duration_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pay_basis: Mapped[str] = mapped_column(String(32), default="", server_default="")
    pay_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pay_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pay_negotiable: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    bio: Mapped[str] = mapped_column(Text, default="", server_default="")
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FamilyProfile(Base):
    __tablename__ = "family_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    display_name: Mapped[str] = mapped_column(String(80), default="", server_default="")
    whatsapp: Mapped[str] = mapped_column(String(32), default="", server_default="")
    photo_url: Mapped[str] = mapped_column(String(400), default="", server_default="")
    area: Mapped[str] = mapped_column(String(80), default="", server_default="")
    children: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    schedule_notes: Mapped[str] = mapped_column(Text, default="", server_default="")
    days_needed: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    hours_per_week: Mapped[int | None] = mapped_column(Integer, nullable=True)
    care_windows: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    start_timing: Mapped[str] = mapped_column(String(32), default="", server_default="")
    duration_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    arrangement: Mapped[str] = mapped_column(String(32), default="", server_default="")
    duties: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    languages_at_home: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    household: Mapped[str] = mapped_column(String(32), default="", server_default="")
    has_pets: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    pet_notes: Mapped[str] = mapped_column(Text, default="", server_default="")
    own_room: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    accommodation_notes: Mapped[str] = mapped_column(Text, default="", server_default="")
    pay_basis: Mapped[str] = mapped_column(String(32), default="", server_default="")
    pay_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pay_negotiable: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    bio: Mapped[str] = mapped_column(Text, default="", server_default="")
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Swipe(Base):
    __tablename__ = "swipes"
    __table_args__ = (
        UniqueConstraint("swiper_id", "target_id", name="uq_swipes_pair"),
        CheckConstraint("direction in ('like', 'pass')", name="ck_swipes_direction"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_id)
    swiper_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    target_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    direction: Mapped[str] = mapped_column(String(8))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("user_low_id", "user_high_id", name="uq_matches_pair"),
        CheckConstraint("user_low_id <> user_high_id", name="ck_matches_distinct"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_id)
    user_low_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    user_high_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
