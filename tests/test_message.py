"""
    test_message
    ~~~~~~~~~~~~

    Contains tests for the :mod:`~adbwp.message` module.
"""
import pytest

from adbwp import consts, enums, header, message, payload


def test_new_computes_header_data_length_based_on_data_payload(command_type, valid_payload_bytes):
    """
    Assert that :func:`~adbwp.message.new` computes and sets the :attr:`~adbwp.header.Header.data_length`
    value based on the given data payload value.
    """
    instance = message.new(command_type, data=valid_payload_bytes)
    assert instance.header.data_length == len(valid_payload_bytes)


def test_new_computes_header_data_checksum_based_on_data_payload(command_type, valid_payload_bytes):
    """
    Assert that :func:`~adbwp.message.new` computes and sets the :attr:`~adbwp.header.Header.data_checksum`
    value based on the given data payload value.
    """
    instance = message.new(command_type, data=valid_payload_bytes)
    assert instance.header.data_checksum == payload.checksum(valid_payload_bytes)


def test_new_computes_header_magic_based_on_data_payload(command_type):
    """
    Assert that :func:`~adbwp.message.new` computes and sets the :attr:`~adbwp.header.Header.magic`
    value based on the given command.
    """
    instance = message.new(command_type)
    assert instance.header.magic == header.magic(command_type)


def test_new_supports_default_values(command_type):
    """
    Assert that :func:`~adbwp.message.new` returns a :class:`~adbwp.message.Message` with the header
    field values set to defaults.
    """
    instance = message.new(command_type)
    assert instance.header.command == command_type
    assert instance.header.arg0 == 0
    assert instance.header.arg1 == 0
    assert instance.data == b''


def test_new_assigns_field_values(command_type, random_arg0, random_arg1, valid_payload_bytes):
    """
    Assert that :func:`~adbwp.message.new` returns a :class:`~adbwp.message.Message` with the header
    and data field values properly set.
    """
    instance = message.new(command_type, random_arg0, random_arg1, valid_payload_bytes)
    assert instance.header.command == command_type
    assert instance.header.arg0 == random_arg0
    assert instance.header.arg1 == random_arg1
    assert instance.data == valid_payload_bytes


def test_new_raises_on_incorrect_payload_type(command_type, invalid_payload_type):
    """
    Assert that :func:`~adbwp.message.new` raises a :class:`~ValueError` when given a payload
    value that is an invalid type.
    """
    with pytest.raises(ValueError):
        message.new(command_type, data=invalid_payload_type)


def test_from_header_assigns_header(command_type, random_arg0, random_arg1):
    """
    Assert that :func:`~adbwp.message.from_header` sets the :attr:`~adbwp.message.Message.header`
    value based on the given header.
    """
    instance = message.from_header(header.new(command_type, random_arg0, random_arg1))
    assert instance.header.command == command_type
    assert instance.header.arg0 == random_arg0
    assert instance.header.arg1 == random_arg1


def test_from_header_raises_on_header_with_incorrect_payload_type(command_type, invalid_payload_type):
    """
    Assert that :func:`~adbwp.message.from_header` raises a :class:`~ValueError` when given a payload
    value that is an invalid type.
    """
    with pytest.raises(ValueError):
        message.from_header(header.new(command_type), data=invalid_payload_type)


def test_connect_assigns_correct_header_field_values():
    """
    Assert that :func:`~adbwp.message.connect` creates a :class:`~adbwp.message.Message` that
    contains a header with the expected field values.
    """
    instance = message.connect('', '')
    assert instance.header.command == enums.Command.CNXN
    assert instance.header.arg0 == consts.VERSION
    assert instance.header.arg1 == consts.CONNECT_AUTH_MAXDATA


def test_connect_sets_system_identity_string_data_payload(random_serial, random_banner, system_type):
    """
    Assert that :func:`~adbwp.message.connect` creates a :class:`~adbwp.message.Message` that
    sets the data payload to a system identity string.
    """
    instance = message.connect(random_serial, random_banner, system_type)
    assert instance.data == payload.system_identity_string(system_type, random_serial, random_banner)
