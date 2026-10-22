from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = BACKEND_ROOT.parent


def env_files() -> tuple[str, ...]:
    found: list[str] = []
    for path in (REPO_ROOT / ".env", BACKEND_ROOT / ".env"):
        if path.exists():
            found.append(str(path))
    return tuple(found)


class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    frontend_origin: str = "http://localhost:3000"
    cookie_secure: bool = False

    model_config = SettingsConfigDict(
        env_file=env_files(),
        extra="ignore",
    )

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgres://"):
            value = "postgresql://" + value[len("postgres://") :]
        scheme, _, rest = value.partition("://")
        if scheme == "postgresql":
            value = f"postgresql+psycopg://{rest}"
        return value

    @field_validator("frontend_origin", mode="before")
    @classmethod
    def strip_origin(cls, value: str) -> str:
        return value.rstrip("/")


settings = Settings()
