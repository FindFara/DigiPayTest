"""Screenshot helpers used by BasePage and pytest failure hooks."""

from datetime import datetime
from pathlib import Path
import re
from playwright.sync_api import Page
from utils.config import settings


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_") or "screenshot"


class ScreenshotManager:
    @staticmethod
    def capture(page: Page, name: str, full_page: bool = True) -> Path:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        path = settings.screenshots_dir / f"{timestamp}_{_safe_name(name)}.png"
        page.screenshot(path=str(path), full_page=full_page)
        return path
