from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "research-agent-os"
    app_env: str = "development"
    log_level: str = "info"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    database_url: str = "postgresql+psycopg://research_agent:research_agent_password@localhost:5432/research_agent_os"

    jwt_secret_key: str = "replace-me-with-a-long-random-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    session_cookie_name: str = "research_agent_os_session"
    cookie_secure: bool = False
    cookie_samesite: str = "lax"

    default_daily_request_limit: int = 10
    default_monthly_request_limit: int = 100
    default_max_tokens_per_request: int = 12000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("api_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()

