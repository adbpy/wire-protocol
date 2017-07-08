"""
    adbwp.message
    ~~~~~~~~~~~~~

    Object representation of a message.
"""
import typing

from . import consts, enums, header, hints, payload


class Message(typing.NamedTuple('Message', [('header', header.Header), ('data', hints.Payload)])):
    """
    Represents an entire ADB protocol message.

    A message consists of a 24-byte header followed by an optional data payload.
    """


def new(command: hints.Command, arg0: int=0, arg1: int=0, data: hints.Payload=b'') -> Message:
    """
    Create a new :class:`~adbwp.message.Message` instance with optional default values.

    :param command: Command identifier
    :type command: :class:`~adbwp.enums.Command` or :class:`~int`
    :param arg0: (Optional) First argument of the command
    :type arg0: :class:`~int`
    :param arg1: (Optional) Second argument of the command
    :type arg1: :class:`~int`
    :param data: (Optional) Message payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Message instance from given values
    :rtype: :class:`~adbwp.message.Message`
    """
    data = payload.as_bytes(data)
    return Message(header.new(command, arg0, arg1, len(data), payload.checksum(data), header.magic(command)), data)


def from_header(header: header.Header, data: hints.Payload=b'') -> Message:  # pylint: disable=redefined-outer-name
    """
    Create a new :class:`~adbwp.message.Message` instance from an existing :class:`~adbwp.header.Header`.

    :param header: Message header
    :type header: :class:`~adbwp.header.Header`
    :param data: (Optional) Message payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Message instance from given values
    :rtype: :class:`~adbwp.message.Message`
    """
    return Message(header, payload.as_bytes(data))


def connect(serial: str, banner: str, system_type: hints.SystemType = enums.SystemType.HOST) -> Message:
    """
    Create a :class:`~adbwp.message.Message` instance that represents a connect message.

    :param serial: Unique identifier
    :type serial: :class:`~str`
    :param banner: Human readable version/identifier string
    :type banner: :class:`~str`
    :param system_type: System type creating the message
    :type system_type: :class:`~adbwp.enums.SystemType` or :class:`~str`
    :return: Message used to connect to a remote system
    :rtype: :class:`~adbwp.message.Message`
    """
    system_identity_string = payload.system_identity_string(system_type, serial, banner)
    return new(enums.Command.CNXN, consts.VERSION, consts.CONNECT_AUTH_MAXDATA, system_identity_string)


def auth_signature(signature: bytes) -> Message:
    """
    Create a :class:`~adbwp.message.Message` instance that represents a signature
    authentication message.

    :param signature: Signed data payload
    :type signature: :class:`~bytes`
    :return: Message used to verify key pair
    :rtype: :class:`~adbwp.message.Message`
    """
    return new(enums.Command.AUTH, enums.AuthType.SIGNATURE, 0, signature)


def auth_rsa_public_key(public_key: bytes) -> Message:
    """
    Create a :class:`~adbwp.message.Message` instance that represents a RSA public key
    authentication message.

    :param public_key: Public key for remote system to conditionally accept
    :type public_key: :class:`~bytes`
    :return: Message used to share public key
    :rtype: :class:`~adbwp.message.Message`
    """
    return new(enums.Command.AUTH, enums.AuthType.RSAPUBLICKEY, 0, payload.null_terminate(public_key))


def open(local_id: int, destination: str) -> Message:  # pylint: disable=redefined-builtin
    """
    Create a :class:`~adbwp.message.Message` instance that represents a open message.

    :param local_id: Stream id on remote system to connect with
    :type local_id: :class:`~int`
    :param destination: Stream destination
    :type destination: :class:`~str`
    :return: Message used to open a stream by id on a remote system
    :rtype: :class:`~adbwp.message.Message`
    :raises ValueError: When local id is zero
    """
    if not local_id:
        raise ValueError('Local id cannot be zero')

    return new(enums.Command.OPEN, local_id, 0, payload.null_terminate(destination))


def ready(local_id: int, remote_id: int) -> Message:
    """
    Create a :class:`~adbwp.message.Message` instance that represents a ready message.

    :param local_id: Identifier for the stream on the local end
    :type local_id: :class:`~int`
    :param remote_id: Identifier for the stream on the remote system
    :type remote_id: :class:`~int`
    :return: Message used to inform remote system it's ready for write messages
    :rtype: :class:`~adbwp.message.Message`
    :raises ValueError: When local id is zero
    :raises ValueError: When remote id is zero
    """
    if not local_id:
        raise ValueError('Local id cannot be zero')
    if not remote_id:
        raise ValueError('Remote id cannot be zero')

    return new(enums.Command.OKAY, local_id, remote_id)


def write(local_id: int, remote_id: int, data: hints.Payload) -> Message:
    """
    Create a :class:`~adbwp.adb.Message` instance that represents a write message.

    :param local_id: Identifier for the stream on the local end
    :type local_id: :class:`~int`
    :param remote_id: Identifier for the stream on the remote system
    :type remote_id: :class:`~int`
    :param data: Data payload sent to the stream
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Message used to write data to remote stream
    :rtype: :class:`~adbwp.message.Message`
    :raises ValueError: When data payload is empty
    """
    if not data:
        raise ValueError('Data cannot be empty')

    return new(enums.Command.WRTE, local_id, remote_id, data)
