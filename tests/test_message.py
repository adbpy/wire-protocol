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
    assert instance.header.data_length == len(valid_payload_bytes)
    assert instance.header.data_checksum == payload.checksum(valid_payload_bytes)
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
    expected = payload.system_identity_string(system_type, random_serial, random_banner)
    instance = message.connect(random_serial, random_banner, system_type)
    assert instance.header.data_length == len(expected)
    assert instance.header.data_checksum == payload.checksum(expected)
    assert instance.data == expected


def test_auth_signature_assigns_correct_header_field_values():
    """
    Assert that :func:`~adbwp.message.auth_signature` creates a :class:`~adbwp.message.Message` that
    contains a header with the expected field values.
    """
    instance = message.auth_signature(b'')
    assert instance.header.command == enums.Command.AUTH
    assert instance.header.arg0 == enums.AuthType.SIGNATURE
    assert instance.header.arg1 == 0


def test_auth_signature_sets_signature_data_payload(random_signature):
    """
    Assert that :func:`~adbwp.message.auth_signature` creates a :class:`~adbwp.message.Message` that
    sets the data payload to the given signature bytes.
    """
    expected = payload.as_bytes(random_signature)
    instance = message.auth_signature(random_signature)
    assert instance.header.data_length == len(expected)
    assert instance.header.data_checksum == payload.checksum(expected)
    assert instance.data == expected


def test_auth_rsa_public_key_assigns_correct_header_field_values():
    """
    Assert that :func:`~adbwp.message.auth_rsa_public_key` creates a :class:`~adbwp.message.Message` that
    contains a header with the expected field values.
    """
    instance = message.auth_rsa_public_key(b'')
    assert instance.header.command == enums.Command.AUTH
    assert instance.header.arg0 == enums.AuthType.RSAPUBLICKEY
    assert instance.header.arg1 == 0


def test_auth_rsa_public_key_sets_public_key_data_payload(random_rsa_public_key):
    """
    Assert that :func:`~adbwp.message.auth_rsa_public_key` creates a :class:`~adbwp.message.Message` that
    sets the data payload to the given RSA public key bytes.
    """
    expected = payload.null_terminate(random_rsa_public_key)
    instance = message.auth_rsa_public_key(random_rsa_public_key)
    assert instance.header.data_length == len(expected)
    assert instance.header.data_checksum == payload.checksum(expected)
    assert instance.data == expected


def test_open_assigns_correct_header_field_values(random_local_id):
    """
    Assert that :func:`~adbwp.message.open` creates a :class:`~adbwp.message.Message` that
    contains a header with the expected field values.
    """
    instance = message.open(random_local_id, '')
    assert instance.header.command == enums.Command.OPEN
    assert instance.header.arg0 == random_local_id
    assert instance.header.arg1 == 0


def test_open_sets_destination_data_payload(random_local_id, random_destination):
    """
    Assert that :func:`~adbwp.message.open` creates a :class:`~adbwp.message.Message` that
    sets the data payload to the given stream destination.
    """
    expected = payload.null_terminate(random_destination)
    instance = message.open(random_local_id, random_destination)
    assert instance.header.data_length == len(expected)
    assert instance.header.data_checksum == payload.checksum(expected)
    assert instance.data == expected


def test_open_raises_on_zero_local_id(random_destination):
    """
    Assert that :func:`~adbwp.message.open` raises a :class:`~ValueError` when given
    a local id value that is zero.
    """
    with pytest.raises(ValueError):
        message.open(0, random_destination)


def test_ready_assigns_correct_header_field_values(random_local_id, random_remote_id):
    """
    Assert that :func:`~adbwp.message.ready` creates a :class:`~adbwp.message.Message` that
    contains a header with the expected field values.
    """
    instance = message.ready(random_local_id, random_remote_id)
    assert instance.header.command == enums.Command.OKAY
    assert instance.header.arg0 == random_local_id
    assert instance.header.arg1 == random_remote_id


def test_ready_assigns_empty_data_payload(random_local_id, random_remote_id):
    """
    Assert that :func:`~adbwp.message.ready` creates a :class:`~adbwp.message.Message` that
    does not have a data payload.
    """
    expected = b''
    instance = message.ready(random_local_id, random_remote_id)
    assert instance.header.data_length == len(expected)
    assert instance.header.data_checksum == payload.checksum(expected)
    assert instance.data == expected


def test_ready_raises_on_zero_local_id(random_remote_id):
    """
    Assert that :func:`~adbwp.message.ready` raises a :class:`~ValueError` when given
    a local id value that is zero.
    """
    with pytest.raises(ValueError):
        message.ready(0, random_remote_id)


def test_ready_raises_on_zero_remote_id(random_local_id):
    """
    Assert that :func:`~adbwp.message.ready` raises a :class:`~ValueError` when given
    a local id value that is zero.
    """
    with pytest.raises(ValueError):
        message.ready(random_local_id, 0)


def test_write_assigns_correct_header_field_values(random_local_id, random_remote_id, valid_payload):
    """
    Assert that :func:`~adbwp.message.write` creates a :class:`~adbwp.message.Message` that
    contains a header with the expected field values.
    """
    instance = message.write(random_local_id, random_remote_id, valid_payload)
    assert instance.header.command == enums.Command.WRTE
    assert instance.header.arg0 == random_local_id
    assert instance.header.arg1 == random_remote_id


def test_write_assigns_given_data_payload(random_local_id, random_remote_id, valid_payload, valid_payload_bytes):
    """
    Assert that :func:`~adbwp.message.write` creates a :class:`~adbwp.message.Message` that
    sets the data payload.
    """
    instance = message.write(random_local_id, random_remote_id, valid_payload)
    assert instance.header.data_length == len(valid_payload_bytes)
    assert instance.header.data_checksum == payload.checksum(valid_payload_bytes)
    assert instance.data == valid_payload_bytes


def test_write_raises_on_empty_data_payload(random_local_id, random_remote_id):
    """
    Assert that :func:`~adbwp.message.write` raises a :class:`~ValueError` when given
    an empty data payload.
    """
    with pytest.raises(ValueError):
        message.write(random_local_id, random_remote_id, b'')


def test_close_assigns_correct_header_field_values(random_local_id, random_remote_id):
    """
    Assert that :func:`~adbwp.message.close` creates a :class:`~adbwp.message.Message` that
    contains a header with the expected field values.
    """
    instance = message.close(random_local_id, random_remote_id)
    assert instance.header.command == enums.Command.CLSE
    assert instance.header.arg0 == random_local_id
    assert instance.header.arg1 == random_remote_id


def test_close_assigns_no_data_payload(random_local_id, random_remote_id):
    """
    Assert that :func:`~adbwp.message.close` creates a :class:`~adbwp.message.Message` that
    has no data payload.
    """
    expected = b''
    instance = message.close(random_local_id, random_remote_id)
    assert instance.header.data_length == len(expected)
    assert instance.header.data_checksum == payload.checksum(expected)
    assert instance.data == expected


def test_close_raises_on_zero_remote_id(random_local_id):
    """
    Assert that :func:`~adbwp.message.ready` raises a :class:`~ValueError` when given
    a local id value that is zero.
    """
    with pytest.raises(ValueError):
        message.close(random_local_id, 0)
