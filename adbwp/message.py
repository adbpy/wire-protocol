"""
    adbwp.message
    ~~~~~~~~~~~~~

    Object representation of a message.
"""
import collections
import typing

from . import consts, enums, header, hints, payload

__all__ = ['Message', 'new', 'from_header', 'connect', 'auth_signature', 'auth_rsa_public_key',
           'open', 'ready', 'write', 'close']


#: Mapping of thee :class:`~adbwp.enums.Command` int value to an :class:`~int` that represents
#: the maximum size of the data payload for the message.
MAX_DATA_LENGTH_BY_COMMAND = collections.defaultdict(lambda: consts.MAXDATA, {
    enums.Command.CNXN.value: consts.CONNECT_AUTH_MAXDATA,
    enums.Command.AUTH.value: consts.CONNECT_AUTH_MAXDATA
})


class Message(typing.NamedTuple('Message', [('header', header.Header), ('data', hints.Buffer)])):
    """
    Represents an entire ADB protocol message.

    A message consists of a 24-byte header followed by an optional data payload.
    """


def new(command: hints.Command, arg0: hints.Int=0, arg1: hints.Int=0, data: hints.Buffer=b'') -> Message:
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
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.MAXDATA`
    """
    data = payload.as_bytes(data)
    return from_header(header.new(command, arg0, arg1, len(data), payload.checksum(data), header.magic(command)), data)


def from_header(header: header.Header, data: hints.Buffer=b'') -> Message:  # pylint: disable=redefined-outer-name
    """
    Create a new :class:`~adbwp.message.Message` instance from an existing :class:`~adbwp.header.Header`.

    :param header: Message header
    :type header: :class:`~adbwp.header.Header`
    :param data: (Optional) Message payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Message instance from given values
    :rtype: :class:`~adbwp.message.Message`
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.MAXDATA`
    """
    data = payload.as_bytes(data)

    max_data_length = MAX_DATA_LENGTH_BY_COMMAND[header.command]
    if len(data) > max_data_length:
        raise ValueError('Data length for {} message cannot be more than {}'.format(header.command, max_data_length))

    return Message(header, data)


def connect(serial: hints.Str, banner: hints.Str, system_type: hints.SystemType=enums.SystemType.HOST) -> Message:
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
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.CONNECT_AUTH_MAXDATA`
    """
    system_identity_string = payload.system_identity_string(system_type, serial, banner)
    return new(enums.Command.CNXN, consts.VERSION, consts.CONNECT_AUTH_MAXDATA, system_identity_string)


def auth_signature(signature: hints.Bytes) -> Message:
    """
    Create a :class:`~adbwp.message.Message` instance that represents a signature
    authentication message.

    :param signature: Signed data payload
    :type signature: :class:`~bytes`
    :return: Message used to verify key pair
    :rtype: :class:`~adbwp.message.Message`
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.CONNECT_AUTH_MAXDATA`
    """
    return new(enums.Command.AUTH, enums.AuthType.SIGNATURE, 0, signature)


def auth_rsa_public_key(public_key: hints.Bytes) -> Message:
    """
    Create a :class:`~adbwp.message.Message` instance that represents a RSA public key
    authentication message.

    :param public_key: Public key for remote system to conditionally accept
    :type public_key: :class:`~bytes`
    :return: Message used to share public key
    :rtype: :class:`~adbwp.message.Message`
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.CONNECT_AUTH_MAXDATA`
    """
    return new(enums.Command.AUTH, enums.AuthType.RSAPUBLICKEY, 0, payload.null_terminate(public_key))


def open(local_id: hints.Int, destination: hints.Str) -> Message:  # pylint: disable=redefined-builtin
    """
    Create a :class:`~adbwp.message.Message` instance that represents a open message.

    :param local_id: Stream id on remote system to connect with
    :type local_id: :class:`~int`
    :param destination: Stream destination
    :type destination: :class:`~str`
    :return: Message used to open a stream by id on a remote system
    :rtype: :class:`~adbwp.message.Message`
    :raises ValueError: When local id is zero
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.MAXDATA`
    """
    if not local_id:
        raise ValueError('Local id cannot be zero')

    return new(enums.Command.OPEN, local_id, 0, payload.null_terminate(destination))


def ready(local_id: hints.Int, remote_id: hints.Int) -> Message:
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
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.MAXDATA`
    """
    if not local_id:
        raise ValueError('Local id cannot be zero')
    if not remote_id:
        raise ValueError('Remote id cannot be zero')

    return new(enums.Command.OKAY, local_id, remote_id)


def write(local_id: hints.Int, remote_id: hints.Int, data: hints.Buffer) -> Message:
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
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.MAXDATA`
    """
    if not data:
        raise ValueError('Data cannot be empty')

    return new(enums.Command.WRTE, local_id, remote_id, data)


def close(local_id: hints.Int, remote_id: hints.Int) -> Message:
    """
    Create a :class:`~adbwp.message.Message` instance that represents a close message.

    :param local_id: Identifier for the stream on the local end
    :type local_id: :class:`~int`
    :param remote_id: Identifier for the stream on the remote system
    :type remote_id: :class:`~int`
    :return: Message used to inform the remote system of stream closing
    :rtype: :class:`~adbwp.message.Message`
    :raises ValueError: When  id is zero
    :raises ValueError: When remote id is zero
    :raises ValueError: When data payload is greater than :attr:`~adbwp.consts.MAXDATA`
    """
    if not remote_id:
        raise ValueError('Remote id cannot be zero')

    return new(enums.Command.CLSE, local_id, remote_id)
