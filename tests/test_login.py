"""BDD entrypoint for login feature scenarios."""

from pytest_bdd import scenarios
from tests.steps.login_steps import *  # noqa: F401,F403 - imported for pytest-bdd step registration

scenarios("login.feature")
