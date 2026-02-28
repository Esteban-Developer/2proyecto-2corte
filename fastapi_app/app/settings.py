from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_secret_key: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    smtp_host: str | None
    smtp_port: int
    smtp_user: str | None
    smtp_password: str | None
    smtp_to_email: str | None

    @property
    def database_url(self) -> str:
        # mysql+pymysql://user:pass@host:port/dbname?charset=utf8mb4
        user = self.db_user
        password = self.db_password
        host = self.db_host
        port = self.db_port
        name = self.db_name
        if password:
            return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"
        return f"mysql+pymysql://{user}@{host}:{port}/{name}?charset=utf8mb4"


def get_settings() -> Settings:
    return Settings(
        app_secret_key=os.getenv("APP_SECRET_KEY", "dev-secret-key"),
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=int(os.getenv("DB_PORT", "3306")),
        db_user=os.getenv("DB_USER", "root"),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_name=os.getenv("DB_NAME", "threaderz_store"),
        smtp_host=os.getenv("SMTP_HOST") or None,
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_user=os.getenv("SMTP_USER") or None,
        smtp_password=os.getenv("SMTP_PASSWORD") or None,
        smtp_to_email=os.getenv("SMTP_TO_EMAIL") or None,
    )

