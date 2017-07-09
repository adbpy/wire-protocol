"""
    conftest
    ~~~~~~~~

    High level fixtures used across multiple test modules.
"""
import os
import random
import string
import sys

import pytest

from adbwp import consts, enums, header, payload


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


@pytest.fixture(scope='session', params=enums.AuthType)
def auth_type(request):
    """
    Fixture that yields all :class:`~adbwp.enums.AuthType` types.
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
def bytes_larger_than_maxdata():
    """
    Fixture that yields collection of bytes larger than :attr:`~adbwp.consts.MAXDATA`.
    """
    return random_bytes(consts.MAXDATA + 1)


@pytest.fixture(scope='session')
def bytes_larger_than_connect_auth_max_data():
    """
    Fixture that yields collection of bytes larger than :attr:`~adbwp.consts.CONNECT_AUTH_MAXDATA`.
    """
    return random_bytes(consts.CONNECT_AUTH_MAXDATA + 1)


@pytest.fixture(scope='session')
def str_larger_than_connect_auth_max_data():
    """
    Fixture that yields a string larger than :attr:`~adbwp.consts.CONNECT_AUTH_MAXDATA`.
    """
    return random_str(consts.CONNECT_AUTH_MAXDATA + 1)


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


@pytest.fixture(scope='session')
def random_serial():
    """
    Fixture that yields a random string value that is usable as the "serial" in a connect message.
    """
    return random_hex_str(16)


@pytest.fixture(scope='session')
def random_banner():
    """
    Fixture that yields a random string value that is usable as the "banner" in a connect message.
    """
    return random_hex_str(32)


@pytest.fixture(scope='session')
def random_signature():
    """
    Fixture that yields a random bytes value that is usable as the "signature" in a auth message.
    """
    return random_bytes(20)


@pytest.fixture(scope='session')
def random_signature():
    """
    Fixture that yields a random bytes value that is usable as the "signature" in a auth message.
    """
    return random_bytes(20)


@pytest.fixture(scope='session')
def random_rsa_public_key():
    """
    Fixture that yields a random bytes value that is usable as the "rsa public key" in a auth message.
    """
    return random_bytes(256)


@pytest.fixture(scope='session')
def random_local_id():
    """
    Fixture that yields a random int value that is usable as the "local id" in a open message.
    """
    return random_int(low=1)


@pytest.fixture(scope='session')
def random_remote_id():
    """
    Fixture that yields a random int value that is usable as the "remote id" in a ready message.
    """
    return random_int(low=1)


@pytest.fixture(scope='session')
def random_destination():
    """
    Fixture that yields a random int value that is usable as the "destination" in a open message.
    """
    return random_str(12)


def random_bytes(length=20):
    """
    Helper function that generates a random collection of bytes.
    """
    return os.urandom(length)


def random_hex_str(length=16):
    """
    Helper function that generates a random hex string.
    """
    return random_str(length, string.hexdigits)


def random_str(length=24, alphabet=string.ascii_letters):
    """
    Helper function that generates a random string.
    """
    return ''.join((random.choice(alphabet) for _ in range(length)))


def random_int(low=0, high=2**31 - 1):
    """
    Helper function that generates a random integer between two values (inclusive).
    """
    return random.randint(low, high)
