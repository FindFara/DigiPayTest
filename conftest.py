"""Pytest fixtures and hooks for browser lifecycle and failure diagnostics."""

from pathlib import Path
import pytest
import allure
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from data.test_data import TestData
from utils.config import settings
from utils.logger import get_logger
from utils.screenshots import ScreenshotManager

logger = get_logger("conftest")


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Launch headless Chromium once per test session for fast, stable runs."""
    with sync_playwright() as playwright:
        logger.info("Launching Chromium. headless=%s slow_mo=%s", settings.headless, settings.slow_mo)
        browser_instance = playwright.chromium.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo,
        )
        yield browser_instance
        browser_instance.close()


@pytest.fixture()
def context(browser: Browser) -> BrowserContext:
    """Create an isolated browser context per scenario to avoid state leakage."""
    context_instance = browser.new_context(
        base_url=settings.base_url,
        locale="fa-IR",
        timezone_id="Asia/Tehran",
        viewport={"width": 1366, "height": 768},
        record_video_dir=str(settings.reports_dir / "videos"),
    )
    context_instance.set_default_timeout(settings.default_timeout)
    yield context_instance
    context_instance.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    """Create a fresh page for each test and expose it to failure hooks."""
    page_instance = context.new_page()
    yield page_instance
    page_instance.close()


@pytest.fixture(scope="session")
def test_data() -> TestData:
    return TestData()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Automatically capture screenshots for failed test calls.

    The hook reads the active `page` fixture only when a test fails, keeping the
    happy path fast while still producing useful diagnostics in screenshots,
    pytest-html and Allure result folders.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page_obj = item.funcargs.get("page")
    if page_obj is None:
        return

    screenshot_path = ScreenshotManager.capture(page_obj, item.nodeid)
    logger.error("Failure screenshot saved: %s", screenshot_path)

    allure.attach.file(
        str(screenshot_path),
        name="failure-screenshot",
        attachment_type=allure.attachment_type.PNG,
    )

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html:
        extra = getattr(report, "extra", [])
        relative_path = Path(screenshot_path).as_posix()
        extra.append(pytest_html.extras.image(relative_path))
        report.extra = extra
