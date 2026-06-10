"""Page Object for direct mobile top-up purchase flow."""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from data.test_data import TopupData


class TopupPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.direct_topup_option = page.get_by_role("button", name="شارژ مستقیم").or_(
            page.get_by_role("link", name="شارژ مستقیم")
        ).or_(page.get_by_test_id("direct-topup"))
        self.phone_input = page.get_by_role("textbox", name="شماره موبایل").or_(
            page.get_by_placeholder("شماره موبایل")
        ).or_(page.get_by_test_id("topup-phone-input"))
        self.operator_dropdown = page.get_by_role("combobox", name="اپراتور").or_(
            page.get_by_test_id("operator-select")
        )
        self.continue_button = page.get_by_role("button", name="ادامه").or_(
            page.get_by_role("button", name="پرداخت")
        ).or_(page.get_by_test_id("topup-submit"))
        self.validation_message = page.get_by_text("شماره موبایل معتبر نیست").or_(
            page.get_by_text("شماره موبایل را به درستی وارد کنید")
        )

    def open_topup(self) -> None:
        self.open("/")
        self.click(
            self.page.get_by_role("link", name="خرید شارژ").or_(
                self.page.get_by_role("button", name="خرید شارژ")
            ).or_(self.page.get_by_test_id("topup-entry"))
        )

    def select_direct_topup(self) -> None:
        self.click(self.direct_topup_option)

    def fill_phone(self, phone_number: str) -> None:
        self.fill(self.phone_input, phone_number)

    def select_operator(self, operator_name: str) -> None:
        try:
            self.click(self.operator_dropdown, timeout=3_000)
            self.click(self.page.get_by_role("option", name=operator_name).or_(self.page.get_by_text(operator_name)))
        except AssertionError:
            self.logger.info("Operator selector was not required or not visible; continuing")

    def select_amount(self, amount: str) -> None:
        amount_locator = self.page.get_by_role("button", name=amount).or_(
            self.page.get_by_text(amount)
        ).or_(self.page.get_by_test_id(f"topup-amount-{amount}"))
        self.click(amount_locator)

    def fill_topup_form(self, data: TopupData) -> None:
        self.fill_phone(data.target_phone)
        self.select_operator(data.operator_name)
        self.select_amount(data.amount)

    def continue_purchase(self) -> None:
        self.click(self.continue_button)

    def expect_checkout_or_login(self) -> None:
        expect(
            self.page.get_by_text("تایید سفارش")
            .or_(self.page.get_by_text("خلاصه سفارش"))
            .or_(self.page.get_by_text("ورود"))
            .or_(self.page.get_by_text("پرداخت"))
        ).to_be_visible(timeout=15_000)

    def expect_validation_error(self) -> None:
        expect(self.validation_message).to_be_visible(timeout=10_000)
