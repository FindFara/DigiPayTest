"""BDD entrypoint for top-up feature scenarios."""

from pytest_bdd import scenarios
from tests.steps.topup_steps import *  # noqa: F401,F403 - imported for pytest-bdd step registration

scenarios("topup.feature")
