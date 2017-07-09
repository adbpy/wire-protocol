"""
    test_header
    ~~~~~~~~~~~

    Contains tests for the :mod:`~adbwp.header` module.
"""
import os

import pytest

from adbwp import consts, enums, exceptions, header

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


@pytest.fixture(scope='session', params=[
    float(),
    list(),
    tuple(),
    dict(),
    set(),
    None
])
def invalid_field_value(request):
    """
    Fixture that yields values that are not the correct type for field values
    of a :class:`~adbwp.header.Header`.
    """
    return request.param


@pytest.fixture(scope='session', params=range(0, 23))
def invalid_bytes_too_few(request):
    """
    Fixture that yields :class:`~bytes` with a length less than 24.
    """
    return os.urandom(request.param)


@pytest.fixture(scope='session', params=range(25, 32))
def invalid_bytes_too_many(request):
    """
    Fixture that yields :class:`~bytes` with a length greater than 24.
    """
    return os.urandom(request.param)


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


def test_header_new_supports_default_values(command_type):
    """
    Assert that :func:`~adbwp.header.new` returns a :class:`~adbwp.header.Header` with the field values
    set to defaults.
    """
    instance = header.new(command_type)
    assert instance.command == command_type
    assert instance.arg0 == 0
    assert instance.arg1 == 0
    assert instance.data_length == 0
    assert instance.data_checksum == 0


def test_header_new_assigns_fields(command_type, random_arg0, random_arg1, random_data_length, random_data_checksum):
    """
    Assert that :func:`~adbwp.header.new` returns a :class:`~adbwp.header.Header` with the field values
    properly set.
    """
    instance = header.new(command_type, random_arg0, random_arg1, random_data_length, random_data_checksum)
    assert instance.command == command_type
    assert instance.arg0 == random_arg0
    assert instance.arg1 == random_arg1
    assert instance.data_length == random_data_length
    assert instance.data_checksum == random_data_checksum


def test_header_magic_computes_command_xor(command_type):
    """
    Assert that :func:`~adbwp.header.magic` XOR's the command value will :attr:`~adbwp.consts.COMMAND_MASK`.
    """
    assert header.magic(command_type) == command_type ^ consts.COMMAND_MASK


def test_header_to_bytes_returns_24_bytes(random_header):
    """
    Assert that :func:`~adbwp.header.to_bytes` converts the given :class:`~adbwp.header.Header` to
    a collection of 24 bytes.
    """
    to_bytes = header.to_bytes(random_header)
    assert len(to_bytes) == 24


def test_header_to_bytes_raises_on_header_with_invalid_field_type(command_type, invalid_field_value):
    """
    Assert that :func:`~adbwp.header.to_bytes` raises a :class:`~adbwp.exceptions.PackError` when
    the :class:`~adbwp.header.Header` contains field values that are not integers.
    """
    with pytest.raises(exceptions.PackError):
        header.to_bytes(header.new(command_type, arg0=invalid_field_value))


def test_header_to_bytes_raises_on_header_with_integer_overflow(command_type):
    """
    Assert that :func:`~adbwp.header.to_bytes` raises a :class:`~adbwp.exceptions.PackError` when
    the :class:`~adbwp.header.Header` contains an integer field value greater than 32-bits.
    """
    with pytest.raises(exceptions.PackError):
        header.to_bytes(header.new(command_type, arg0=2**32 + 1))


def test_header_from_bytes_raises_on_less_than_24_bytes(invalid_bytes_too_few):
    """
    Assert that :func:`~adbwp.header.from_bytes` raises a :class:`~adbwp.exceptions.UnpackError` when
    given a :class:`~bytes` instance that is less than 24 bytes long.
    """
    with pytest.raises(exceptions.UnpackError):
        header.from_bytes(invalid_bytes_too_few)


def test_header_from_bytes_raises_on_more_than_24_bytes(invalid_bytes_too_many):
    """
    Assert that :func:`~adbwp.header.from_bytes` raises a :class:`~adbwp.exceptions.UnpackError` when
    given a :class:`~bytes` instance that is more than 24 bytes long.
    """
    with pytest.raises(exceptions.UnpackError):
        header.from_bytes(invalid_bytes_too_many)


def test_header_from_bytes_converts_command_to_enum(random_header_bytes):
    """
    Assert that :func:`~adbwp.header.from_bytes` converts the command bytes to a
    :class:`~adbwp.enums.Command` instance.
    """
    instance_from_bytes = header.from_bytes(random_header_bytes)
    assert isinstance(instance_from_bytes.command, enums.Command)


def test_header_converts_to_from_bytes(random_header, random_header_bytes):
    """
    Assert that a :class:`~adbwp.header.Header` that is converted to :class:`~bytes` and back
    maintains fidelity to the original instance.
    """
    instance_from_bytes = header.from_bytes(random_header_bytes)
    assert instance_from_bytes == random_header
