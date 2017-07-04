"""
    test_header
    ~~~~~~~~~~~

    Contains tests for the :mod:`~adbwp.header` module.
"""
import pytest

from adbwp import enums, header


#: Names of properties on the :class:`~adbwp.header.Header` class that shortcut checks for determining
#: the command type.
#: Note: This order must match the enum value definition order of :class:`~adbwp.enums.Command`.
HEADER_COMMAND_PROPERTY_NAMES = ['sync', 'connect', 'auth', 'open', 'ready', 'close', 'write']


#: Names of properties on the :class:`~adbwp.header.Header` class that shortcut checks for determining
#: the command response type.
#: Note: This order must match the enum value definition order of :class:`~adbwp.enums.CommandResponse`.
HEADER_COMMAND_RESPONSE_PROPERTY_NAMES = ['okay', 'fail']


@pytest.fixture(scope='session', params=list(zip(HEADER_COMMAND_PROPERTY_NAMES, enums.Command)))
def property_name_with_command(request):
    """
    Fixture that yields valid command types paired with the name of the property defined on
    :class:`~adbwp.header.Header` that checks it.
    """
    return request.param


@pytest.fixture(scope='session', params=list(zip(HEADER_COMMAND_RESPONSE_PROPERTY_NAMES, enums.CommandResponse)))
def property_name_with_command_response(request):
    """
    Fixture that yields valid command response types paired with the name of the property defined on
    :class:`~adbwp.header.Header` that checks it.
    """
    return request.param


def test_header_property_check_matches_command_type(property_name_with_command):
    """
    Assert that the properties defined on :class:`~adbwp.header.Header` that check the command value
    return :bool:`~True` as expected.
    """
    name, value = property_name_with_command
    instance = header.new(value)
    assert getattr(instance, name)


def test_header_property_check_matches_command_response_type(property_name_with_command_response):
    """
    Assert that properties defined on :class:`~adbwp.header.Header` that check the command response value
    return :bool:`~True` as expected.
    """
    name, value = property_name_with_command_response
    instance = header.new(value)
    assert getattr(instance, name)
