"""Page Object for DigiPay login behavior."""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.login_button = page.get_by_role("button", name="ورود").or_(
            page.get_by_role("link", name="ورود")
        ).or_(page.get_by_test_id("login-button"))
        self.phone_input = page.get_by_role("textbox", name="شماره موبایل").or_(
            page.get_by_placeholder("شماره موبایل")
        ).or_(page.get_by_test_id("phone-number-input"))
        self.continue_button = page.get_by_role("button", name="ادامه").or_(
            page.get_by_test_id("submit-login")
        )
        self.otp_input = page.get_by_role("textbox", name="کد تایید").or_(
            page.get_by_test_id("otp-input")
        )
        self.validation_message = page.get_by_text("شماره موبایل معتبر نیست").or_(
            page.get_by_text("شماره موبایل را به درستی وارد کنید")
        )

    def open_login(self) -> None:
        self.open("/")
        try:
            self.click(self.login_button, timeout=5_000)
        except AssertionError:
            self.logger.info("Login trigger was not visible on home page; opening /login directly")
            self.open("/login")

    def enter_phone_number(self, phone_number: str) -> None:
        self.fill(self.phone_input, phone_number)

    def submit(self) -> None:
        self.click(self.continue_button)

    def login_with_phone(self, phone_number: str) -> None:
        self.enter_phone_number(phone_number)
        self.submit()

    def expect_otp_step(self) -> None:
        expect(
            self.page.get_by_text("کد تایید").or_(self.page.get_by_text("رمز یکبار مصرف")).or_(self.otp_input)
        ).to_be_visible(timeout=15_000)

    def expect_validation_error(self) -> None:
        expect(self.validation_message).to_be_visible(timeout=10_000)
