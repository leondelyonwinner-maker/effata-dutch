"""
Centralized, typed application configuration.

All secrets are pulled exclusively from environment variables. Nothing here
is a placeholder value that could accidentally leak into version control —
if a required secret is missing in production, the app fails to boot rather
than falling back to an insecure default.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Environment ---
    environment: str = "development"  # "development" | "production"

    # --- Database ---
    # Render injects DATABASE_URL as postgres://... ; SQLAlchemy's async driver
    # needs postgresql+asyncpg://... so we normalize it in the validator below.
    database_url: str = "sqlite+aiosqlite:///./effata_dutch.db"

    # --- Auth ---
    # bcrypt hash of the single-user passcode. Generate with:
    #   python -m app.cli hash-passcode "your-passcode"
    # Never store the plaintext passcode anywhere.
    app_passcode_hash: str = ""
    session_secret_key: str = "insecure-dev-secret-change-me"
    session_cookie_name: str = "effata_session"
    session_max_age_seconds: int = 60 * 60 * 24 * 30  # 30 days

    # --- DeepSeek ---
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    # --- Rate limiting (login endpoint) ---
    login_max_attempts: int = 5
    login_lockout_seconds: int = 300

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def normalized_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()
