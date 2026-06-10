"""Page Object for home page navigation."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.topup_entry = page.get_by_role("link", name="خرید شارژ").or_(
            page.get_by_role("button", name="خرید شارژ")
        ).or_(page.get_by_test_id("topup-entry"))

    def open_home(self) -> None:
        self.open("/")

    def go_to_topup(self) -> None:
        self.click(self.topup_entry)
