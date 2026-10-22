from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20261022_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("role in ('candidate', 'family')", name="ck_users_role"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "candidate_profiles",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("display_name", sa.String(80), nullable=False, server_default=""),
        sa.Column("whatsapp", sa.String(32), nullable=False, server_default=""),
        sa.Column("photo_url", sa.String(400), nullable=False, server_default=""),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("gender", sa.String(32), nullable=False, server_default=""),
        sa.Column("nationality", sa.String(80), nullable=False, server_default=""),
        sa.Column("based_in", sa.String(120), nullable=False, server_default=""),
        sa.Column("languages", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("experience_years", sa.Integer(), nullable=True),
        sa.Column("experience_age_bands", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("experience_summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("qualification", sa.String(160), nullable=False, server_default=""),
        sa.Column("first_aid", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("garda_vetting", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("has_references", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("smoker", sa.Boolean(), nullable=True),
        sa.Column("comfortable_with_pets", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("has_driving_licence", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("has_own_car", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("eu_passport", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("special_needs_experience", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("duties", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("arrangement", sa.String(32), nullable=False, server_default=""),
        sa.Column("areas", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("minds_in", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("days_available", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("hours_per_week", sa.Integer(), nullable=True),
        sa.Column("schedule_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("available_short_notice", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("start_timing", sa.String(32), nullable=False, server_default=""),
        sa.Column("duration_months", sa.Integer(), nullable=True),
        sa.Column("pay_basis", sa.String(32), nullable=False, server_default=""),
        sa.Column("pay_min", sa.Integer(), nullable=True),
        sa.Column("pay_max", sa.Integer(), nullable=True),
        sa.Column("pay_negotiable", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("bio", sa.Text(), nullable=False, server_default=""),
        sa.Column("is_complete", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_table(
        "family_profiles",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("display_name", sa.String(80), nullable=False, server_default=""),
        sa.Column("whatsapp", sa.String(32), nullable=False, server_default=""),
        sa.Column("photo_url", sa.String(400), nullable=False, server_default=""),
        sa.Column("area", sa.String(80), nullable=False, server_default=""),
        sa.Column("children", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("schedule_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("days_needed", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("hours_per_week", sa.Integer(), nullable=True),
        sa.Column("care_windows", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("start_timing", sa.String(32), nullable=False, server_default=""),
        sa.Column("duration_months", sa.Integer(), nullable=True),
        sa.Column("arrangement", sa.String(32), nullable=False, server_default=""),
        sa.Column("duties", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("languages_at_home", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("household", sa.String(32), nullable=False, server_default=""),
        sa.Column("has_pets", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("pet_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("own_room", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("accommodation_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("pay_basis", sa.String(32), nullable=False, server_default=""),
        sa.Column("pay_amount", sa.Integer(), nullable=True),
        sa.Column("pay_negotiable", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("bio", sa.Text(), nullable=False, server_default=""),
        sa.Column("is_complete", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_table(
        "swipes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("swiper_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("direction", sa.String(8), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("direction in ('like', 'pass')", name="ck_swipes_direction"),
        sa.UniqueConstraint("swiper_id", "target_id", name="uq_swipes_pair"),
    )
    op.create_index("ix_swipes_swiper_id", "swipes", ["swiper_id"])
    op.create_index("ix_swipes_target_id", "swipes", ["target_id"])
    op.create_table(
        "matches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_low_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_high_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("user_low_id <> user_high_id", name="ck_matches_distinct"),
        sa.UniqueConstraint("user_low_id", "user_high_id", name="uq_matches_pair"),
    )
    op.create_index("ix_matches_user_low_id", "matches", ["user_low_id"])
    op.create_index("ix_matches_user_high_id", "matches", ["user_high_id"])


def downgrade() -> None:
    op.drop_table("matches")
    op.drop_table("swipes")
    op.drop_table("family_profiles")
    op.drop_table("candidate_profiles")
    op.drop_table("users")
