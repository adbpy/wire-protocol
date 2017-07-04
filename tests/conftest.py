"""
    conftest
    ~~~~~~~~

    High level fixtures used across multiple test modules.
"""
import pytest

from adbwp import enums


@pytest.fixture(scope='session', params=enums.Command)
def command_type(request):
    """
    Fixture that yields all :class:`~adbwp.enums.Command` types.
    """
    return request.param
