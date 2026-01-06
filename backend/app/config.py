"""Application configuration with Pydantic compatibility across v1/v2.

This module attempts to import BaseSettings from whichever package
is available so importing `app` during tests doesn't fail when the
environment has Pydantic v2 (where BaseSettings moved to
`pydantic-settings`).
"""
import os
from typing import Any
from pathlib import Path

try:
    # Pydantic v1 (and modern v2 backwards compat in some envs)
    from pydantic import BaseSettings  # type: ignore
except Exception:
    # Pydantic v2 moved settings to pydantic-settings package
    try:
        from pydantic_settings import BaseSettings  # type: ignore
    except Exception:  # pragma: no cover - fallback if neither is available
        # If neither pydantic.BaseSettings nor pydantic_settings.BaseSettings
        # is available (e.g., in minimal test envs), provide a tiny fallback
        # so importing `app` doesn't fail. This fallback will not provide
        # validation; it's meant purely for test/development runtime.
        class BaseSettings:  # type: ignore
            def __init__(self, **_: Any) -> None:  # pragma: no cover - runtime fallback
                # nothing to do; Settings class will have class-level defaults
                return

# Try to load a local .env file (app/.env) when available so developers can
# keep secrets and environment configuration out of source files. This is
# optional and will silently continue if python-dotenv is not installed.
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.joinpath('.env')
    if env_path.exists():
        load_dotenv(str(env_path))
except Exception:
    # dotenv not installed or failed to load; continue using os.environ
    pass


class Settings(BaseSettings):
    # Secrets should live in the environment (.env for local development).
    # Avoid providing real defaults here to prevent accidental leaks.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    SECURITY_PASSWORD_SALT: str = os.getenv("SECURITY_PASSWORD_SALT", "")

    # Database config - prefer explicit DATABASE_URL in the environment
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Admin / blockchain config
    ADMIN_ADDRESS: str = os.getenv("ADMIN_ADDRESS", "")
    ADMIN_PRIVATE_KEY: str = os.getenv("ADMIN_PRIVATE_KEY", "")
    RPC_URL: str = os.getenv("RPC_URL", "http://127.0.0.1:7545")  # local default

    # Email / SendGrid settings
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
    EMAIL_RETRY_MAX_ATTEMPTS: int = int(os.getenv("EMAIL_RETRY_MAX_ATTEMPTS", "5"))
    EMAIL_RETRY_BASE_DELAY_SECONDS: int = int(os.getenv("EMAIL_RETRY_BASE_DELAY_SECONDS", "60"))

    # OAuth settings
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Metrics & alerting
    METRICS_ENABLED: bool = bool(int(os.getenv("METRICS_ENABLED", "1")))
    SLACK_WEBHOOK_URL: str = os.getenv("SLACK_WEBHOOK_URL", "")

    # Database logging: explicitly set DATABASE_LOGGING to 0/1 in env to control SQL logs.
    # If it's not set, default to enabled when DATABASE_URL points to PostgreSQL.
    _db_logging_env = os.getenv("DATABASE_LOGGING", None)
    if _db_logging_env not in (None, ""):
        DATABASE_LOGGING: bool = bool(int(_db_logging_env))
    else:
        DATABASE_LOGGING: bool = "postgresql" in os.getenv("DATABASE_URL", "")


settings = Settings()

# Backwards compatibility: some modules expect BLOCKCHAIN_RPC_URL
if not hasattr(settings, "BLOCKCHAIN_RPC_URL"):
    try:
        settings.BLOCKCHAIN_RPC_URL = getattr(settings, "RPC_URL")
    except Exception:
        settings.BLOCKCHAIN_RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:7545")

