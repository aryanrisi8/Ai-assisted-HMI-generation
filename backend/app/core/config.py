from functools import lru_cache

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI-Assisted Adaptive HMI Platform"
    app_env: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    log_format: str = "json"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "hmi_platform"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    database_url: str | None = None

    jwt_secret_key: str = Field(
        default="change-this-secret-before-production",
        min_length=16,
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    backend_cors_origins: list[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> str:
        uri = self.database_url or (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        if uri.startswith("postgres://"):
            return uri.replace("postgres://", "postgresql+psycopg://", 1)
        if uri.startswith("postgresql://"):
            return uri.replace("postgresql://", "postgresql+psycopg://", 1)
        return uri

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug", "development"}:
                return True
            if normalized in {"0", "false", "no", "off", "release", "production"}:
                return False
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
