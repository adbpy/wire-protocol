"""
    test_payload
    ~~~~~~~~~~~~

    Contains tests for the :mod:`~adbwp.payload` module.
"""
import pytest

from adbwp import consts, payload


def test_checksum_computes_sum_bitwse_and_mask(valid_payload_bytes):
    """
    Assert that :func:`~adbwp.payload.checksum` computes the expected value.
    """
    assert payload.checksum(valid_payload_bytes) == sum(valid_payload_bytes) & consts.COMMAND_MASK


def test_null_terminate_adds_zero_byte(valid_payload, valid_payload_bytes):
    """
    Assert that :func:`~adbwp.payload.null_terminate` adds a zero-byte to the end of the data payload.
    """
    assert payload.null_terminate(valid_payload) == valid_payload_bytes + b'\0'


def test_null_terminate_raises_on_incorrect_payload_type(invalid_payload_type):
    """
    Assert that :func:`~adbwp.payload.null_terminate` raises a :class:`~ValueError` when given a data
    payload value that is an invalid type.
    """
    with pytest.raises(ValueError):
        payload.null_terminate(invalid_payload_type)


def test_as_bytes_converts_supported_types_to_bytes(valid_payload):
    """
    Assert that :func:`~adbwp.payload.as_bytes` converts any valid data payload value to :class:`~bytes`.
    """
    assert isinstance(payload.as_bytes(valid_payload), (bytes, bytearray))


def test_as_bytes_raises_on_incorrect_payload_type(invalid_payload_type):
    """
    Assert that :func:`~adbwp.payload.as_bytes` raises a :class:`~ValueError` when given a data
    payload value that is an invalid type.
    """
    with pytest.raises(ValueError):
        payload.as_bytes(invalid_payload_type)


def test_system_identity_string_colon_delimites_values(system_type, random_serial, random_banner):
    """
    Assert that :func:`~adbwp.payload.system_identity_string` adds a ":" delimiter between the values.
    """
    instance = payload.system_identity_string(system_type, random_serial, random_banner)
    assert instance.decode().count(':') == 2


def test_system_identity_string_null_terminates(system_type, random_serial, random_banner):
    """
    Assert that :func:`~adbwp.payload.system_identity_string` adds a zero-byte to the end.
    """
    instance = payload.system_identity_string(system_type, random_serial, random_banner)
    assert instance[-1] == 0
