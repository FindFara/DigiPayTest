"""pytest-bdd step definitions for top-up scenarios."""

from pytest_bdd import given, then, when
from data.test_data import TestData
from pages.topup_page import TopupPage
from utils.config import settings


@given("the user is on the top-up page")
def open_topup_page(page):
    topup_page = TopupPage(page)
    topup_page.open_topup()
    return topup_page


@when("the user selects direct top-up")
def select_direct_topup(open_topup_page: TopupPage):
    open_topup_page.select_direct_topup()


@when("the user completes the top-up form with valid data")
def complete_topup_form(open_topup_page: TopupPage):
    topup_data = TestData.topup(settings.phone_number)
    open_topup_page.fill_topup_form(topup_data)


@when("the user enters an invalid top-up phone number")
def enter_invalid_topup_phone(open_topup_page: TopupPage):
    topup_data = TestData.topup(settings.phone_number)
    open_topup_page.fill_phone("0912")
    open_topup_page.select_operator(topup_data.operator_name)
    open_topup_page.select_amount(topup_data.amount)


@when("the user continues the top-up purchase")
def continue_topup_purchase(open_topup_page: TopupPage):
    open_topup_page.continue_purchase()


@then("the checkout or login step should be displayed")
def checkout_or_login_should_be_displayed(open_topup_page: TopupPage):
    open_topup_page.expect_checkout_or_login()


@then("a top-up validation error should be displayed")
def topup_validation_error_should_be_displayed(open_topup_page: TopupPage):
    open_topup_page.expect_validation_error()
