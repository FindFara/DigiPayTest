"""Base page object with reusable Playwright operations.

Architecture decision: page objects expose business-friendly actions while this
base class owns low-level interactions, waiting and screenshots. This keeps
selectors centralized and step definitions free of browser implementation detail.
"""

from pathlib import Path
from typing import Union
from playwright.sync_api import Locator, Page, expect
from utils.config import settings
from utils.logger import get_logger
from utils.screenshots import ScreenshotManager

Selector = Union[str, Locator]


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(self.__class__.__name__)
        self.page.set_default_timeout(settings.default_timeout)

    def open(self, path: str = "/") -> None:
        url = f"{settings.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.logger.info("Opening URL: %s", url)
        self.page.goto(url, wait_until="domcontentloaded")

    def _locator(self, selector: Selector) -> Locator:
        if isinstance(selector, str):
            return self.page.locator(selector)
        return selector

    def wait_for_element(self, selector: Selector, timeout: int | None = None) -> Locator:
        locator = self._locator(selector).first()
        self.logger.info("Waiting for element: %s", selector)
        expect(locator).to_be_visible(timeout=timeout or settings.default_timeout)
        return locator

    def click(self, selector: Selector, timeout: int | None = None) -> None:
        locator = self.wait_for_element(selector, timeout)
        self.logger.info("Clicking element: %s", selector)
        locator.click()

    def fill(self, selector: Selector, value: str, timeout: int | None = None) -> None:
        locator = self.wait_for_element(selector, timeout)
        self.logger.info("Filling element with value length %s", len(value))
        locator.fill(value)

    def get_text(self, selector: Selector, timeout: int | None = None) -> str:
        locator = self.wait_for_element(selector, timeout)
        text = locator.inner_text()
        self.logger.info("Element text: %s", text)
        return text

    def take_screenshot(self, name: str) -> Path:
        self.logger.info("Capturing screenshot: %s", name)
        return ScreenshotManager.capture(self.page, name)
