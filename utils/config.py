"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://app.mydigipay.com")
    phone_number: str = os.getenv("PHONE_NUMBER", "09123456789")
    otp: str = os.getenv("OTP", "12345")
    headless: bool = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes", "y"}
    slow_mo: int = int(os.getenv("SLOW_MO", "0"))
    default_timeout: int = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
    screenshots_dir: Path = ROOT_DIR / "screenshots"
    reports_dir: Path = ROOT_DIR / "reports"


settings = Settings()
settings.screenshots_dir.mkdir(parents=True, exist_ok=True)
settings.reports_dir.mkdir(parents=True, exist_ok=True)
