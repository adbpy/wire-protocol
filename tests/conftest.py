"""
    conftest
    ~~~~~~~~

    High level fixtures used across multiple test modules.
"""
import pytest
import random
import string
import sys

from adbwp import enums, header, payload


@pytest.fixture(scope='session', params=enums.Command)
def command_type(request):
    """
    Fixture that yields all :class:`~adbwp.enums.Command` types.
    """
    return request.param


@pytest.fixture(scope='session', params=enums.SystemType)
def system_type(request):
    """
    Fixture that yields all :class:`~adbwp.enums.SystemType` types.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    b'foo',
    b'foobar',
    'foo',
    'foobar',
    bytearray(b'foo'),
    bytearray(b'foobar'),
    memoryview(b'foobar'),
    memoryview(b'foobar'),
    int(1024).to_bytes(4, byteorder='little'),
    sys.maxsize.to_bytes(8, byteorder='little')
])
def valid_payload(request):
    """
    Fixture that yields valid data payload values.
    """
    return request.param


@pytest.fixture(scope='session')
def valid_payload_bytes(valid_payload):
    """
    Fixture that yields valid data payloads as :class:`~bytes`.
    """
    return payload.as_bytes(valid_payload)


@pytest.fixture(scope='session', params=[
    int(),
    list(),
    set(),
    dict(),
    tuple()
])
def invalid_payload_type(request):
    """
    Fixture that yields data payload values of unsupported types.
    """
    return request.param


@pytest.fixture(scope='session')
def random_header(command_type, random_arg0, random_arg1, random_data_length,
                  random_data_checksum, command_type_magic):
    """
    Fixture that yields a :class:`~adbwp.header.Header` instance for each :class:`~adbwp.enums.Command`
    type and with random values.
    """
    return header.new(command_type, random_arg0, random_arg1, random_data_length,
                      random_data_checksum, command_type_magic)


@pytest.fixture(scope='session')
def random_header_bytes(random_header):
    """
    Fixture that yields a :class:`~bytes` instance that represents a header.
    """
    return header.to_bytes(random_header)


@pytest.fixture(scope='session')
def command_type_magic(command_type):
    """
    Fixture that yields the computed "magic" value of the given command type.
    """
    return header.magic(command_type)


@pytest.fixture(scope='session')
def random_arg0():
    """
    Fixture that yields a random integer value that is usable as "arg0" in a :class:`~adbwp.header.Header`.
    """
    return random_int()


@pytest.fixture(scope='session')
def random_arg1():
    """
    Fixture that yields a random integer value that is usable as "arg1" in a :class:`~adbwp.header.Header`.
    """
    return random_int()


@pytest.fixture(scope='session')
def random_data_length():
    """
    Fixture that yields a random integer value that is usable as "data_length" in a :class:`~adbwp.header.Header`.
    """
    return random_int()


@pytest.fixture(scope='session')
def random_data_checksum():
    """
    Fixture that yields a random integer value that is usable as "data_checksum" in a :class:`~adbwp.header.Header`.
    """
    return random_int()


def random_int(x=0, y=2**31 - 1):
    """
    Helper function that generates a random integer between two values (inclusive).
    """
    return random.randint(x, y)
