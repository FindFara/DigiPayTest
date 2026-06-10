"""Centralized test data.

Keeping data outside tests and page objects prevents hard-coded values from
spreading through the framework and makes future data providers (JSON, DB,
API fixtures) easy to plug in.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LoginData:
    valid_phone: str
    invalid_phone: str = "0912"


@dataclass(frozen=True)
class TopupData:
    target_phone: str
    amount: str = "20000"
    operator_name: str = "همراه اول"


class TestData:
    """Factory for scenario data used by step definitions."""

    @staticmethod
    def login(valid_phone: str) -> LoginData:
        return LoginData(valid_phone=valid_phone)

    @staticmethod
    def topup(target_phone: str) -> TopupData:
        return TopupData(target_phone=target_phone)
