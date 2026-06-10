"""pytest-bdd step definitions for login scenarios."""

from pytest_bdd import given, then, when
from data.test_data import TestData
from pages.login_page import LoginPage
from utils.config import settings


@given("the user is on the login page")
def open_login_page(page):
    login_page = LoginPage(page)
    login_page.open_login()
    return login_page


@when("the user submits a valid phone number")
def submit_valid_phone(open_login_page: LoginPage):
    open_login_page.login_with_phone(settings.phone_number)


@when("the user submits an invalid phone number")
def submit_invalid_phone(open_login_page: LoginPage):
    invalid_phone = TestData.login(settings.phone_number).invalid_phone
    open_login_page.login_with_phone(invalid_phone)


@then("the OTP step should be displayed")
def otp_step_should_be_displayed(open_login_page: LoginPage):
    open_login_page.expect_otp_step()


@then("a login validation error should be displayed")
def login_validation_error_should_be_displayed(open_login_page: LoginPage):
    open_login_page.expect_validation_error()
