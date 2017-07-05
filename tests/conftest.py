"""
    conftest
    ~~~~~~~~

    High level fixtures used across multiple test modules.
"""
import pytest
import random

from adbwp import enums, header


@pytest.fixture(scope='session', params=enums.Command)
def command_type(request):
    """
    Fixture that yields all :class:`~adbwp.enums.Command` types.
    """
    return request.param


@pytest.fixture(scope='session')
def random_header(command_type, random_arg0, random_arg1, random_data_length,
                  random_data_checksum, command_type_magic):
    """
    Fixture that yields a :class:`~adbwp.header.Header` instance for each :enum:`~adbwp.enums.Command`
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
