from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = f"sqlite:///{DATA_DIR / 'bet_admin.db'}"
    MONGODB_URL: str = "mongodb+srv://visionmember54_db_user:m2tBvaFeikpWS1Cy@cluster0.t3a9ka9.mongodb.net/kalyandb?retryWrites=true&w=majority"
    MONGODB_DB_NAME: str = "kalyandb"

    @field_validator("DATABASE_URL")
    @classmethod
    def _normalize_postgres_scheme(cls, value: str) -> str:
        # If Render or env still has an old dead postgres connection string or dpg- host,
        # ignore it and use the local SQLite cache powered by MongoDB Atlas.
        if "dpg-" in value or "onrender.com" in value or value.startswith("postgres"):
            return f"sqlite:///{DATA_DIR / 'bet_admin.db'}"
        return value



    # No default: the app must fail to boot if this isn't set explicitly.
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    JWT_TTL_MIN: int = 480

    # "production" hides the interactive API docs.
    APP_ENV: str = "development"

    CORS_ORIGINS: str = "http://localhost:3000"
    LOGIN_MAX_FAILURES: int = 5
    LOGIN_LOCK_MINUTES: int = 15

    # Firebase Phone Auth: verifies the ID token the app gets after Firebase itself
    # sends and checks the SMS code. Prefer the JSON-in-an-env-var form on Render
    # (Secret Files require a paid plan); fall back to a local file for dev.
    FIREBASE_SERVICE_ACCOUNT_JSON: str | None = None
    FIREBASE_SERVICE_ACCOUNT_PATH: str = str(BASE_DIR / "secrets" / "firebase-service-account.json")

    # OTP delivery: one fixed physical device (a dedicated phone with a SIM,
    # running a small relay app) receives {appName, phoneNumber, otp} as an
    # FCM data message and sends the actual SMS via its own SmsManager. This
    # is a single global token, not a per-user one -- real SMS delivery
    # without paying a commercial SMS gateway.
    OTP_RELAY_DEVICE_FCM_TOKEN: str | None = None
    OTP_RELAY_APP_NAME: str = "kalyan"

    @property
    def cors_origins_list(self) -> list[str]:
        # A wildcard origin is invalid together with credentials, so it is never honoured.
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip() and o.strip() != "*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
