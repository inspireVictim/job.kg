from __future__ import annotations

from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    PROJECT_NAME: str = "Corporate Portal"
    API_V1_PREFIX: str = "/api"

    SECRET_KEY: str = "diploma-corporate-portal-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 часа

    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'portal.db'}"

    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    MAX_UPLOAD_SIZE: int = 20 * 1024 * 1024  # 20 MB

    CORS_ORIGINS: List[str] = [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "null",
        "*",
    ]


settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
