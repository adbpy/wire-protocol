"""
    test_enums
    ~~~~~~~~~~

    Contains tests for the :mod:`~adbwp.enums` module.
"""
import pytest

from adbwp import enums


@pytest.mark.parametrize(('enum_value', 'int_value'), list(zip(enums.Command, (0x434e5953, 0x4e584e43, 0x48545541,
                                                                               0x4e45504f, 0x59414b4f, 0x45534c43,
                                                                               0x45545257))))
def test_command_values_unchanged(enum_value, int_value):
    """
    Assert that the :class:`~adbwp.enums.Command` integer values remain unchanged. The goal of this
    test is to guard against an _accidental_ value change as it will require the test to be modified to pass.
    """
    assert enum_value.value == enum_value == int_value


@pytest.mark.parametrize(('enum_value', 'int_value'), list(zip(enums.AuthType, (1, 2, 3))))
def test_auth_type_values_unchanged(enum_value, int_value):
    """
    Assert that the :class:`~adbwp.enums.AuthType` integer values remain unchanged. The goal of this
    test is to guard against an _accidental_ value change as it will require the test to be modified to pass.
    """
    assert enum_value.value == enum_value == int_value


@pytest.mark.parametrize(('enum_value', 'str_value'), list(zip(enums.CommandResponse, ('OKAY', 'FAIL'))))
def test_command_response_str_returns_value(enum_value, str_value):
    """
    Assert that :class:`~adbwp.enums.CommandResponse` defines :meth:`~adbwp.enums.CommandResponse.__str__`
    and returns the individual enum value.
    """
    assert enum_value.value == str(enum_value) == str_value


@pytest.mark.parametrize(('enum_value', 'str_value'), list(zip(enums.SystemType, ('bootloader', 'device', 'host'))))
def test_system_type_str_returns_value(enum_value, str_value):
    """
    Assert that :class:`~adbwp.enums.SystemType` defines :meth:`~adbwp.enums.SystemType.__str__`
    and returns the individual enum value.
    """
    assert enum_value.value == str(enum_value) == str_value
